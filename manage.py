#!/bin/python3
import sys

import shutil
from LatexZettel import files, database
import re
import os
import peewee as pw


class Helper:

    def help():
        print("""

            Manage the LaTeX slip box. This file should never be executed with the working directory not the base directory of the slipbox project.
        """)

    def addtodocuments(filename, reference=""):
        """
            Adds line \externaldocument[reference-]{filename} to documents.tex
            If reference is not supplied then it defaults to, for example, NoteName if filename=note_name
        """
            

        with open('notes/documents.tex', 'a') as f:
            f.write(f'\externaldocument[{reference}-]{{{filename}}}\n')



    def getnotefiles(directory='notes'):
        notes = [str(f) for f in files.get_files(directory)]
        return notes

    def createnotefile(filename):
        try:
            os.mkdir('notes')
        except FileExistsError:
            pass

        try:
            os.mkdir('notes/slipbox')
        except FileExistsError:
            pass


        try:
            with open(f'notes/{filename}.tex') as f:
                pass
        except FileNotFoundError:
            shutil.copyfile('template/note.tex', f'notes/slipbox/{filename}.tex')
            return

        print(f'File notes/{filename}.tex already exists, skipping copying the template')
    

    def newnote(note_name, reference_name=""):
        """
            createnote note_name [Optional ReferenceName]
            Creates note with name note_name.tex, Second argument is optional and is the name in the reference, defaults to NoteName

            to do: check whether a file already exists etc

        """
        if reference_name == "":
            reference_name = ''.join([w.capitalize() for w in note_name.split('_')])
        
        #see if the note already exists
        try:
            note = database.Note.get(filename=note_name)
            raise ValueError(f'A note with file name {filename} already exists in the database. If this is not the case then run manage.py synchronize to update the database, and then try again')
            return 
        except pw.OperationalError:
            database.create_all_tables()
        except database.Note.DoesNotExist:
            try: 
                note = database.Note.get(reference=reference_name)
                raise ValueError(f'A note with reference {reference} already exists in the database. If this is not the case then run manage.py synchronize to update the database, and then try again. If the problem persists check the documents.tex file is correctly setup')
                return
            except database.Note.DoesNotExist:
                pass


        
    
        Helper.createnotefile(note_name)
        Helper.addtodocuments(note_name, reference_name)
        #once created, add note to database 
        note = database.Note(filename=note_name, reference=reference_name)
        note.save()

    def renderallhtml():
        """
            Renderes all the notes using make4ht. Saves output in /html
        """

        notes = Helper.getnotefiles()
        try:
            os.mkdir('html')
        except FileExistsError:
            pass
        os.chdir('html')

        for note in notes:
            filename = note[:-4] 
            os.system(f'make4ht ../{note} svg')
            os.system(f'biber {filename}')

        for note in notes:
            filename = note[:-4] 
            os.system(f'make4ht ../{note} svg')
       
       
    def renderallpdf():
        """
            Renderes all the notes using pdflatex. Saves output in /pdf
        """
        
        notes = Helper.getnotefiles()
        try:
            os.mkdir('pdf')
        except FileExistsError:
            pass
        os.chdir('pdf')

        for note in notes:
            filename = note[:-4] 
            os.system(f'pdflatex ../{note} svg')
            os.system(f'biber {filename}')

        for note in notes:
            filename = note[:-4] 
            os.system(f'pdflatex ../{note} svg')


    def getyesno():
        while True:
            a = input()
            if a == 'y':
                return True
            elif a == 'n':
                return False
            else:
                print('Please enter either \'y\' or \'n\'')

    def synchronize():
        """
            Reads the file documents.tex and adds these files to the database, then checks for files in /notes that aren't in the documents
        """

        notes = ['notes/'.join(str(f).split('notes/')[1:])[:-4] for f in files.get_files('notes')]
        #get all the tracked notes
        tracked_notes = {}
        with open('documents.tex', 'r') as f:
            for line in f:
                m = re.search('(\\\\externaldocument\[)(.+?)(\-\]\{)(.+?)(\})', line)
                if m:
                    reference_name = m.group(2)
                    filename = m.group(4)

                    if filename not in notes:
                        print(f'File {filename} with reference {reference_name} missing from notes. Make new note now? (y/n)')
                        if Helper.getyesno():
                            Helper.createnotefile(filename)
                            tracked_notes[filename] = reference_name
                            
                    else:
                        tracked_notes[filename] = reference_name

        for filename, reference_name in tracked_notes.items():
            try:
                note = database.Note.get(filename=filename)
                if note.reference == reference_name:
                    continue #nothing to do
            except database.Note.DoesNotExist:
                try:
                    note = database.Note.get(reference=filename)
                except database.Note.DoesNotExist:
                    #create the note if there are no close matches
                    note = database.Note(filename=filename, reference=reference_name)



        for note in notes:
            if note not in tracked_notes:
                print(f'File {note} not tracked by the file documents.tex. Add to the file now? (y/n)')
                if Helper.getyesno(): 
                    reference = ''.join([w.capitalize() for w in note.split('_')])
                    print(f'Reference (defaults to {reference}):', end='')
                    reference = input()
                    Helper.addtodocuments(note, reference)





    def getlabels():
        notes = Helper.getnotefiles()
        for note in notes:
            with open(f'{note}') as f:
                for line in f:
                    labels = re.search('(\\\\label\{)(.*?)(\})', line)
                    try:
                        label = labels.group(2)
                        print(label)
                    except AttributeError:
                        pass



    def getlinks():
        notes = Helper.getnotefiles()
        for note in notes:
            with open(note) as f:
                for line in f:
                    links = re.finditer('\\\\ex(hyper)?(c)?ref\{(.*?)\}\{(.*?)\}', line)

                    for link in links:
                        print(f'file: {link.group(3)}, label referenced {link.group(4)}')

    def gettags():
        notes = Helper.getnotefiles()
        tags = {}
        for note in notes:
            with open(note) as f:
                lines = f.read().splitlines()
                last_line = lines[-1]
                if re.search("\\\\end\{document\}", last_line) is None:
                    note_tags = [f.lower() for f in last_line.strip().split(",")]
                    for tag in note_tags:
                        print(note)
                        tags[tag] = ('notes/'.join(note.split('notes/')[1:]))[:-4]


        print(tags)


                        




def main(args):
    try:
        func = args[1]
    except IndexError:
        print(f"No argument passed, try '{args[0]} help'")
        return

    try: 
        function = getattr(Helper, func)
    except AttributeError:
        print(f"Unregognised command {args[1]}, try 'help' for a list of availlable commands")

    function(*args[2:])




if __name__ == "__main__":
    main(sys.argv)
