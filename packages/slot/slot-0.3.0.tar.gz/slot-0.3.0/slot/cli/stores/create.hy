(import click)
(import [click [echo style secho]])

(import [slot.store [Store]])

(with-decorator
  (.command click)
  (.argument click "name")
  (.argument click "target")
  (defn create [name target]
    (setv obj (Store name))
    (if obj.registered
        (do
          (echo
            (.format
              "Store {} is already installed!"
              (style (.name obj) :fg "red" :bold True)))))

    (.create obj target)

    (echo
      (.format
        "Successfully created store: {} -> {}"
        (style obj.name :fg "green" :bold True)
        (style obj.target :fg "green" :bold True)))

    (if (.confirm click "Do you want to move the current file into the store?")
        (do
          (setv new-name
                (.prompt click "Please enter a name for this option (e.g. default)" :confirmation-prompt True))
          (.ingest obj new-name :link True)
          (secho "Done!" :fg "green" :bold True)))))
