(import os)
(import click)

(import [slot.store [Store]])

(with-decorator
  (.command click)
  (.argument click "store_name")
  (.argument click "file_name")
  (.option click "-n" "--name" :type click.STRING :default None :help "Name of the option this file becomes")
  (.option click "-s" "--silent" :type click.BOOL :help "Disable user interaction")
  (defn ingest [store-name file-name name silent]
    (setv store (Store store-name))
    (setv new-name (or name (os.path.basename file-name)))

    (if
      (and (none? name) (not silent))
      (if
        (not
          (.confirm
            click
            (.format "Is the name {} okay for this option?" (.style click new-name :bold True))))
        (setv new-name (.prompt click "Please choose a new name"))))

    (.ingest store new-name :file-name file-name)

    (.secho click "Done!" :fg "green" :bold True)))
