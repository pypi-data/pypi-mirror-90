(import os)

(setv ROOT-DIR (os.path.expanduser (os.environ.get "SLOT_DATA_DIR" "~/.slot")))
(setv STORES-DIR (os.path.join ROOT-DIR "stores"))
