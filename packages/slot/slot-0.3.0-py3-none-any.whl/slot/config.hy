(import os)

(import [box [Box]])
(import [ruamel.yaml [YAML]])

(import [.constants [ROOT-DIR]])

(setv yaml (YAML :typ "safe"))
(setv yaml.default-flow-style False)

(setv file-name "config.yml")
(setv file-path (os.path.join ROOT-DIR file-name))

(defclass Config []
  (defn --new-- [self]
    (try
      (return (.load Config))
      (except [FileNotFoundError] None))

    (.dump Config (Box {"stores" {}}))
    (.load Config))

  (with-decorator
    classmethod
    (defn load [cls]
      (with [f (open file-path)]
        (Box
          (.load yaml (.read f))))))

  (with-decorator
    classmethod
    (defn dump [cls data]
      (with [f (open file_path "w")]
        (.dump yaml (.to_dict data) f)))))
