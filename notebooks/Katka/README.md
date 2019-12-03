prezentace.ipynb obsahuje rozpracovaný postup pro transfer learning, uložení modelu natrénované sítě a vytvoření funkce, 
která z path k obrázku tento obrázek klasifikuje buď jako rajče nebo jablko

transfer_cnn.ipynb je zúžení postupu rozebraného v prezentace.ipynb pouze k natrénování sítě a uložení modelu 
(občas síť nezkonverguje, je třeba projet celý program znovu, pardon :–( )

klasifikator.ipynb je zúžení postupu rozebraného v prezentace.ipynb, kde se uploaduje uložený model (model.h5)
na základě předložené cesty k obrázku ho rozřadí do příslušné třídy

pokud spuštěním transfer_cnn.ipynb nebo prezentace.ipynb nepřepíšete model.h5, který jsem uploadovala já, 
klasifikator.ipynb by vám měl fungovat pro problém jablko vs. rajče 
(zkoušela jsem i na obrázky, které jsou barevně/tvarově odlišné než ty z training množiny a vše fungovalo)
