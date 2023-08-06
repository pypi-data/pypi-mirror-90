(import click)
(import [click [echo style]])

(import [slot.config [Config]])
(import [slot.store [Store]])

(with-decorator
  (.command click)
  (defn list-stores []
    (setv
      stores
      (lfor name (.stores.keys (Config)) (Store name)))

    (for
      [store stores]
      (echo
        (.format
          "{} -> {}{}"

          (style store.name :fg "cyan" :bold True)

          (style
            (if store.registered "installed" "not installed")
            :fg (if store.registered "green" "red")
            :bold True)

          (style
            (if store.registered (.format " [{}]" store.selected-option) "")
            :fg "blue"
            :bold True))))))
