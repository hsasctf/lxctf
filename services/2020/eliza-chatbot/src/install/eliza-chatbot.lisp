#!/usr/bin/sbcl --script
;; start this with nohup ./eliza-chatbot.lisp &
;; load requirements
(load "/home/eliza-chatbot/quicklisp/setup.lisp")
(ql:quickload "cl-who")
(ql:quickload "hunchentoot")
(ql:quickload "parenscript")
(ql:quickload "mito")
(ql:quickload "sxql")
(ql:quickload "qbase64")
(ql:quickload "flexi-streams")
(ql:quickload "ironclad")

;;;; -------------------------------------------------------------
;;;; Database
;;;; -------------------------------------------------------------
;; connect to database
(mito:connect-toplevel :sqlite3 :database-name "eliza-web.db")

;; session ids are autoincemented in sessions
(defclass session ()
  ((cookie :col-type (or (:varchar 128) :null)
	   :initarg :cookie
	   :accessor :user-cookie))
  (:metaclass mito:dao-table-class)
  (:record-timestamps nil))
(mito:ensure-table-exists 'session)

(defclass protocol ()
  ((message :col-type (or (:varchar 512) :null)
	    :initarg :message
	    :accessor :protocol-message)
   (session :col-type session
	    :initarg :session
	    :accessor :message-session))
  (:metaclass mito:dao-table-class)
  (:record-timestamps nil)
  (:auto-pk nil))

;; create tables
(mito:ensure-table-exists 'protocol)

(defun create-session-in-db (cookie)
  (mito:create-dao 'session :cookie cookie))

(defun get-session-from-cookie (cookie)
  (return-from get-session-from-cookie (mito:find-dao 'session :cookie cookie)))

(defun get-id-from-cookie (cookie)
  (return-from get-id-from-cookie
    (mito:object-id (mito:find-dao 'session :cookie cookie))))

(defun reduce-input (input maxlen)
  (let* ((len (length input)) (max maxlen))
    (if (< 0 (- len max))
	(return-from reduce-input (subseq input (- len max) len))
	(return-from reduce-input input))))

(defun insert-user-message (cookie message)
  (let* ((decode-message (handler-case (qbase64:decode-string message)
			   (error () nil))))
    (if (and decode-message (> 127 (elt decode-message 1)) (< 31 (elt decode-message 1)))
	(progn
	  (let* ((tmp-message (handler-case (flexi-streams:octets-to-string decode-message  :external-format :utf-8)
				(error () nil))))
	    (if tmp-message
		(mito:create-dao 'protocol :session (mito:find-dao 'session :cookie cookie) :message (reduce-input (format nil "~a" (handler-case (funcall tmp-message) (error () tmp-message))) 500)))))
	(mito:create-dao 'protocol :session (mito:find-dao 'session :cookie cookie) :message (reduce-input message 50)))))

(defun get-user-messages-from-db (cookie)
  (return-from get-user-messages-from-db
    (mito:select-dao 'protocol
      (sxql:where (:= :session (get-session-from-cookie cookie))))))

(defun get-all-protocols-from-db ()
  (return-from get-all-protocols-from-db
    (mito:select-dao 'protocol
      (sxql:order-by :session (:desc :id)))))

(defun get-stringified-messages (cookie)
  (let* ((output nil))
    (dolist (message (get-user-messages-from-db cookie))
      (let* ((item (slot-value message 'message)))
	(setq output (append output (list item)))))
    (return-from get-stringified-messages output)))

(defun get-stringified-protocols ()
  (let* ((output nil))
    (dolist (protocol (get-all-protocols-from-db))
      (let* ((item (slot-value protocol 'message)))
	(setq output (append output (list item)))))
    (return-from get-stringified-protocols output)))

(defun delete-user-entries (cookie)
  (mito:delete-dao (get-session-from-cookie cookie)))

(defun create-hash-value (input-string)
  (let* ((output-string (ironclad:byte-array-to-hex-string
			 (ironclad:digest-sequence :sha256 (flexi-streams:string-to-octets input-string)))))
    (return-from create-hash-value output-string)))

(defun verify-token (token)
  (let* ((out-message nil))
    (when (or (string= (create-hash-value token) "4e47826698bb4630fb4451010062fadbf85d61427cbdfaed7ad0f23f239bed89") (string= (create-hash-value token) "ec2a3c9ff29bd6c14dbde1fdfeddd4a1691cc0b80f7060a2bb7900d78d93902b"))
      (setq out-message (get-stringified-protocols)))
    (return-from verify-token out-message)))

(defun get-last-message (message)
  (let* ((len (- (length message) 1)))
    (if (> len -1)
	(return-from get-last-message (list (nth len message)))
	(return-from get-last-message (list "Start your chat!")))))

(defun user-identified (id)
  (if (>= (parse-integer id) 1)
      (return-from user-identified t)
      (return-from user-identified nil)))

;;;; -------------------------------------------------------------
;;;; Frontend
;;;; -------------------------------------------------------------
(defmacro standard-page ((&key title messages id) &body body)
  `(who:with-html-output-to-string (html nil :prologue "<!doctype html>")
     (:html :lang "en"
	    (:head
	     (:meta :http-equiv "Content-Type" 
		    :content    "text/html;charset=utf-8")
	     (:title ,title)
	     (:link :type "text/css"
		    :rel "stylesheet"
		    :href "/eliza.css"))
	    (:body
	     (:div :id "header"
		   (:h1 "ELIZA WEB CHAT")
		   (:h4 "I am ELIZA. I am here to help with your depression.")
		   (:h4 "If you don't feel like chatting anymore, just type 'bye' and ENTER."))
	     (:div :id "conversation-record"
		   (:a :id "conversation-link" :href (concatenate 'string "/conversation?id=" (format nil "~a" ,id)) "Go to your chat progress"))
	     (:div :id "message-box"
		   (loop for string in ,messages
		      do (who:htm
			  (:p :class "message" (who:htm (who:esc string))))))
	     (:div :id "input-form"
		   (:form
		    (:input :type "text" :name "reply" :size "100"))
		   ,@body)))))

(defmacro result-page ((&key title) &body body)
  `(who:with-html-output-to-string (html nil :prologue "<!doctype html>")
     (:html :lang "en"
	    (:head
	     (:meta :http-equiv "Content-Type" 
		    :content    "text/html;charset=utf-8")
	     (:title ,title)
	     (:link :type "text/css"
		    :rel "stylesheet"
		    :href "/eliza.css"))
	    (:body
	     (:div :id "header"
		   (:h1 "ELIZA WEB CHAT - Conversation record")
		   (:div :id "chat"
			 (:p (:a :id "chat-link" :href "/" "Go back to the chat.")))
		   (loop for string in ,@body
		      do (who:htm
			  (:p :class "message" (who:htm (who:esc string))))))))))

(defmacro error-page ((&key title) &body body)
  `(who:with-html-output-to-string (html nil :prologue "<!doctype html>")
     (:html :lang "en"
	    (:head
	     (:meta :http-equiv "Content-Type" 
		    :content    "text/html;charset=utf-8")
	     (:title ,title)
	     (:link :type "text/css"
		    :rel "stylesheet"
		    :href "/eliza.css"))
	    (:body
	     (:div :id "header"
		   (:h1 "ELIZA WEB CHAT - THIS IS AN ERROR")
		   (:div :id "chat"
			 (:p (:a :id "chat-link" :href "/" "Go back to the chat.")))
		   ,@body)))))


;;;; -------------------------------------------------------------
;;;; Eliza chatbot
;;;; -------------------------------------------------------------

(defparameter *bindings* nil)

(defun match (pat in)
  (if (null pat) 
      (null in)
      (if (eq (first pat) '*)
	  (wildcard pat in)
	  (if (eq (first pat) (first in))
	      (match (rest pat) (rest in))
	      nil))))

(defun wildcard (pat in)
  (if (match (rest (rest pat)) in)
      (progn (setf *bindings*
		   (bind (first (rest pat)) nil *bindings*))
	     t)
      (if (null in)
	  nil 
	  (if (match pat (rest in))
	      (progn (setf *bindings* 
			   (bind (first (rest pat)) (first in) *bindings*))
		     t)
	      nil))))

(defun bind (var value bindings)
  (if (null bindings) 
      (list (if value (list var value) (list var)))
      (let* ((key (first (first bindings)))
	     (values (rest (first bindings)))
	     (new (swap value)))
	(if (eq var key)
	    (cons (cons key (cons new values)) (rest bindings))
	    (cons (first bindings) (bind var new (rest bindings)))))))

(defun lookup (key alist)
  (if (null alist) nil
      (if (eq (first (first alist)) key)
	  (first alist)
	  (lookup key (rest alist)))))

(defparameter *viewpoint* '((I you) (you I) (me you) (am are) (was were) (my your)))

(defun swap (value)
  (let* ((a (lookup value *viewpoint*)))
    (if a (first (rest a)) value)))

(defun subs (list)
  (if (null list)
      nil
      (let* ((a (lookup (first list) *bindings*)))
	(if a
	    (append (rest a) (subs (rest list)))
	    (cons (first list) (subs (rest list)))))))

(defparameter *rules*
  '(((* x hello * y) (hello. how can I help ?))
    ((* x i want * y) (what would it mean if you got y ?) (why do you want y ?))
    ((* x i wish * y) (why would it be better if y ?))
    ((* x i hate * y) (what makes you hate y ?))
    ((* x if * y)
     (do you really think it is likely that y)
     (what do you think about y))
    ((* x no * y) (why not?))
    ((* x i was * y) (why do you say x you were y ?))
    ((* x i feel * y) (do you often feel y ?))
    ((* x i felt * y) (what other feelings do you have?))
    ((* x) (you say x ?) (tell me more.))))

(defun random-elt (list)
  (nth (random (length list)) list))

;; this is where the magic happens
;; generates output out of input
(defun eliza (cookie message)
  (if (string= message "bye")
      (progn
	(insert-user-message cookie "Stopping session. Bye.")
	(return-from eliza t))
      (insert-user-message cookie message))
  (setq *bindings* nil)
  (let* ((input (list message)))
    (dolist (r *rules*)
      (when (match (first r) input)
	(insert-user-message cookie (concatenate 'string "ELIZA: " (format nil "~{~(~a ~)~}" (subs (random-elt (rest r))))))
	(return nil)))))



;;;; -------------------------------------------------------------
;;;; hunchentoot based functions
;;;; -------------------------------------------------------------
;; the actual webserver
(defvar *eliza-web-server* (make-instance 'hunchentoot:easy-acceptor :port 5104))
(hunchentoot:start *eliza-web-server*)

;; handler for main page
(hunchentoot:define-easy-handler (display-cookie :uri "/") (reply)
  (setf (hunchentoot:content-type*) "text/html")
  (if (string= (hunchentoot:cookie-in "finished") "true")
      (progn
	(hunchentoot:set-cookie "finished" :value "false" :http-only t)
	(delete-user-entries (hunchentoot:session-cookie-value hunchentoot:*session*))
	(hunchentoot:remove-session hunchentoot:*session*)
	(hunchentoot:redirect "/"))
      (if (hunchentoot:cookie-in "the-high-ground")
	  (let* ((out-message (verify-token (hunchentoot:cookie-in "the-high-ground"))))
	    (progn
	      (let ((session (hunchentoot:start-session))
		    (cookie (hunchentoot:cookie-out "hunchentoot-session")))
		(setf (hunchentoot:session-max-time session) 3600)
		(setf (hunchentoot:session-value 'user session) "ctf-user")
		(setf (hunchentoot:session-value 'pass session) "1234567")
		(when cookie
		  (setf (hunchentoot:cookie-expires
			 (hunchentoot:cookie-out "hunchentoot-session"))
			(+ (get-universal-time) 3600))
		  (create-session-in-db (hunchentoot:session-cookie-value hunchentoot:*session*))))
	      (let* ((cookie (hunchentoot:session-cookie-value hunchentoot:*session*)))
		(if (eq reply nil)
		    ;; no reply, no action
		    ()
		    (when (eliza cookie reply)
		      (let* ((cookie (hunchentoot:session-cookie-value hunchentoot:*session*)))
			(hunchentoot:set-cookie "finished" :value "true" :http-only t)
			(hunchentoot:redirect (concatenate 'string "/conversation?id=" (format nil "~a" (get-id-from-cookie cookie)))))))
		(if out-message
		    (setq out-message (reduce-input out-message 3000))
		    (setq out-message (get-last-message (get-stringified-messages cookie))))
		(format nil "~A" (standard-page (:title "Eliza - Chat" :messages out-message :id (get-id-from-cookie cookie)))))))
	  (progn
	    (hunchentoot:set-cookie "the-high-ground" :value "General Kenobi" :http-only t)
	    (hunchentoot:redirect "/")))))

;; handler for record page
(hunchentoot:define-easy-handler (display-conversation :uri "/conversation") (id)
  (setf (hunchentoot:content-type*) "text/html")
  (let* ((cookie (hunchentoot:session-cookie-value hunchentoot:*session*)))
    (if (user-identified id)
	(format nil "~A" (result-page (:title "Eliza - Conversation") (get-stringified-messages cookie)))
	(format nil "~{~a~}" (get-stringified-protocols)))))

;; handler for error page
(hunchentoot:define-easy-handler (display-error :uri "/error") ()
  (setf (hunchentoot:content-type*) "text/html")
  (hunchentoot:set-cookie "the-high-ground" :value "You are a bold one" :http-only t)
  (format nil "~A" (error-page (:title "Eliza - Error"))))


;; don't delete
;; keeps the server running forever
(loop while t)
