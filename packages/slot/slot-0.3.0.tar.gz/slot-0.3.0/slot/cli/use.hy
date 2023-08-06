(import click)
(import [click [echo style secho]])

(import [slot.store [Store]])

(with-decorator
  (.command click)
  (.argument click "store_name")
  (.argument click "option")
  (defn use [store-name option]
    (setv store (Store store-name))

    (echo
      (.format "Registering {} in {}"
               (style option :fg "cyan" :bold True)
               (style store-name :fg "cyan" :bold True)))

    (.select store option)

    (secho "Done!" :fg "green" :bold True)))
