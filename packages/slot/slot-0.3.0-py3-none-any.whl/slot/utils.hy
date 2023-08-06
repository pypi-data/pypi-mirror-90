(import [glob [glob]])
(import [use-dir [use-dir]])

(import [.store [Store]])
(import [.constants [STORES-DIR]])

(defn get-all-stores []
  (with [(use-dir STORES-DIR)]
    (lfor d (glob "*") (Store d))))
