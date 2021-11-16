import csv
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from time import strftime
import json

class Parse():
    def __init__(self, pasrseFile , folderDestination):
        self.parseFile = pasrseFile
        self.fileDestination = folderDestination
        self.import_index = { 
        "sku" : 0,
        "name" : 1,
        "tag_ids" : 2,
        "category_ids" : 3,
        "price": 4,
        "tax_class" : 5,
        "stock_quantitiy": 6,
        }
        self.woocommerce_fieldnames = ['id',
                                'type',
                                'sku',
                                'name',
                                'published',
                                'catalog_visibility',
                                'short_description',
                                'description',
                                'tax_status',
                                'tax_class',
                                'stock_status',
                                'backorders',
                                'sold_individually',
                                'reviews_allowed',
                                'purchase_note',
                                'price',
                                'stock_quantity',
                                'category_ids',
                                'tag_ids']
        #self.CsvWriteHeader()
        #clear le fichier erreur
        #permet de clear le fichier erreur
        f = open("error.txt", 'w')
        f.write("")
        f.close()

    def CsvWriteHeader(self):
        # ecrire l'entete csv correspondant a woocomerce 
        csv_file = open(self.fileDestination,'w')
        self.csv_writer = csv.DictWriter(csv_file, fieldnames=self.woocommerce_fieldnames, delimiter=';')
        self.csv_writer.writeheader()
        

    def PasrseFile(self):
        with open(self.fileDestination, 'w', newline='') as csvfile:
            fieldnames = self.woocommerce_fieldnames
            self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            self.writer.writeheader()
            i=0
            with open(self.parseFile, "r", encoding="utf8") as self.parseFileObject:
                for line in self.parseFileObject:
                    print(i)
                    self.ParseLine(line)
                    i+=1

    def ParseLine(self, line):
        # remplacement des @ par ; puis split au ;
        line_strip= line.strip('\n')
        line_strip = str(line_strip).replace('@', ';')
        line_split = line_strip.split(';')
        #print(line_split)
        if len(line_split) < 7:
            #print("produit non renseigné")
            with open("error.txt", 'a') as error:
                error.write(line+"/n")
        else:
            self.csvWrite(line_split)

    def csvWrite(self, line_split):
        # complete le csv avec valeur par default si non renseigné dans export.txt

            dict = {}
            
            ##csv_writer.writeheader()
            #self.csv_writer.writeheader(csvfile, fieldnames=self.woocommerce_fieldnames)
            for field in self.woocommerce_fieldnames:
                if field in self.import_index:
                    #print(self.import_index[field])
                    dict[field] = line_split[self.import_index[field]]
                else:
                    #print("default value")
                    dict[field] = " "
            #print(dict)
            self.writer.writerow(dict)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.csv_path= "" 
        self.txt_path = ""
    def mainScreen(self):
        self.rowconfigure(6, weight=3)
        self.columnconfigure(5,weight=1)
        self.button("choisir fichier source", self.choose_txt , 1 , 4, 'blue' )
        self.button("choisir dossier destination", self.choose_csv , 2 ,4 , 'orange')
        self.button("NEXT", self.proceed , 3 , 4, bg='#54FA9B')

    def button(self, texte, fct, row , column, bg):
        bouton=tk.Button(self, text=texte, command=fct)
        bouton.grid(row= row, column=column)

    def choose_txt(self):
        FILETYPES = [ ("txt files", "*.txt") ]
        self.txt_path = askopenfilename(filetypes=FILETYPES)

    def printError(self):
        self.clearAll()
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0,weight=1)
        self.printText("export fini")
        nb_erreur = self.getNombreErreur()
        self.printText("{} produit(s) n'a (ont) pas été importé".format(nb_erreur))
        if nb_erreur !=0:
            with open('error.txt', 'r') as error:
                for erreur in error:
                    self.printText(erreur)
        
    def printText(self, texte):
        txt = tk.Label(text=texte)
        txt.pack()

    def getNombreErreur(self):
        i=0
        with open('error.txt', 'r') as erreurs:
            for line in erreurs:
                i+=1
        return i

    def clearAll(self):
        print("clear all")
        print(self.winfo_children())
        for iteme in self.winfo_children():
            iteme.destroy()

    def choose_csv(self):
        name= "/export.csv"
        self.csv_path = filedialog.askdirectory()+name
        print(self.csv_path)

    def proceed(self):
        if self.csv_path != "" and self.txt_path != "":
            parse= Parse(self.txt_path , self.csv_path)
            parse.PasrseFile()
            self.printError()
            print("done")
        else:
            print("pas complet")



if __name__ == "__main__":
    app = App()
    app.geometry("300x75")
    app.configure(bg='white')
    app.title("Import La Guilde des joueurs")
    app.mainScreen()
    app.mainloop()
