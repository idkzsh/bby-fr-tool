import pandas as pd
import translators as ts
import re


# _ = ts.preaccelerate_and_speedtest()
class BBYTranslator:
    """
    BBYTranslator Class takes an input excel file, translates the data into a dataframe
    and using the translators library, translates the data either in it's entirety or word by word.

    It also removes vowels and spaces from any titles that exceed the character limits
    """

    def __init__(self, callback_function, row_callback):
        """Initializer method for BBYTranslator Class

        Args:
            callback_function (function): callback function to the update_treeview function in the TranslatorApp Class
            row_callback (function): callback function to the update_total_rows function in the TranslatorApp Class
            [These may be deleted and reworked as I want to minimize coupling]
        """
        self.callback_function = callback_function
        self.callback_row = row_callback
        self.total_rows = 0
        self.count = 0

    def read_file(self, input_file, mode):
        """Read file method inserts the data from the excel file into the dataframe,
        then one of two translation methods depending on which translator mode was selected in the TranslatorApp Class

        Args:
            input_file (str): The file path for the input excel file
            mode (int): the translation mode, if 1, translate by entire SKU. if 2, translate word by word.
        """

        df = pd.read_excel(input_file)
        self.total_rows = len(df)
        file_path_index = input_file.rfind("/")
        directory_path = input_file[:file_path_index]
        output_file = directory_path + "translated_data.xlsx"

        if mode == 1:
            df["SKU_DESC FRENCH"] = df.apply(
                self.translate_sku,
                column_name_fr="SKU_DESC FRENCH",
                column_name="SKU_DESC",
                chars=40,
                axis=1,
            )
            df["SHORT_DESC FRENCH"] = df.apply(
                self.translate_sku,
                column_name_fr="SHORT_DESC FRENCH",
                column_name="SHORT_DESC",
                chars=20,
                axis=1,
            )
        elif mode == 2:
            df["SKU_DESC FRENCH"] = df.apply(
                self.translate_word,
                column_name_fr="SKU_DESC FRENCH",
                column_name="SKU_DESC",
                chars=40,
                axis=1,
            )
            df["SHORT_DESC FRENCH"] = df.apply(
                self.translate_word,
                column_name_fr="SHORT_DESC FRENCH",
                column_name="SHORT_DESC",
                chars=20,
                axis=1,
            )
        elif mode == 3:
            df["OUTPUT"] = df.apply(
                self.shorten,
                axis=1,
                chars=40,
                col_name = "SKU_DESC",
                col_name_short = "OUTPUT"
            )

        df.to_excel(output_file, index=False)
        return output_file

    def translate_sku(self, row, column_name_fr, column_name, chars):
        """Translate SKU method takes the entire SKU and translates it together to help the translator understand context of words

        Args:
            row (int): the current row index of the dataframe
            column_name_fr (str): The name of the column that the translation will be output to
            column_name (str): the name of the column that the method will be translating
            chars (int): if it exceeds, the character limit that the translation will be shortened to

        Returns:
            str: the translation
        """
        abbreviations = {
            "blk": "black",
            "clr": "clear",
            "gry": "gray",
            "grn": "green",
            "wht": "white",
            "prp": "purple",
            "blu": "blue",
            "crm": "crimson",
        }

        if pd.isnull(row[column_name_fr]):
            desc_fr = ""
            desc = row[column_name]

            words = desc.split()

            brand = words[0] + " "
            words = words[1:]

            sentence = " ".join(words)

            for abbr, full_word in abbreviations.items():
                if re.search(rf"\b{abbr}\b", sentence, re.IGNORECASE):
                    sentence = re.sub(
                        rf"\b{abbr}\b", full_word, sentence, flags=re.IGNORECASE
                    )

            desc_fr = ts.translate_text(sentence, from_language="en", to_language="fr")

            desc_fr = desc_fr.upper()

            # Define the pattern to match "(EN ANGLAIS SEULEMENT)"
            pattern = r"\(EN ANGLAIS SEULEMENT\)"

            # Use re.sub to replace the pattern with an empty string
            desc_fr = re.sub(pattern, "", desc_fr)

            if len(desc_fr) > chars - len(brand):
                while len(desc_fr) > chars - len(brand):
                    modified = False

                    desc_fr, modified = self.remove_chars(desc_fr)

                    if not modified:
                        break

            desc_fr = brand + desc_fr

            tree_result = [row["SKU"], desc, desc_fr]

            self.count += 1
            self.callback_function(tree_result)
            self.callback_row(self.count, self.total_rows)
            return desc_fr

    def translate_word(self, row, column_name_fr, column_name, chars):
        """Translate word method takes the entire SKU and translates it word by word,
        this is better at translating each word but can lose the context and also the translation is usually too long

        Args:
            row (int): the current row index of the dataframe
            column_name_fr (str): The name of the column that the translation will be output to
            column_name (str): the name of the column that the method will be translating
            chars (int): if it exceeds, the character limit that the translation will be shortened to

        Returns:
            str: the translation
        """
        abbreviations = {
            "blk": "black",
            "clr": "clear",
            "gry": "gray",
            "grn": "green",
            "wht": "white",
            "prp": "purple",
            "blu": "blue",
            "crm": "crimson",
        }

        if pd.isnull(row[column_name_fr]):
            desc_fr = ""
            desc = row[column_name]

            words = desc.split()

            brand = words[0] + " "
            words = words[1:]

            for word in words:
                if not word.isdigit():
                    for abbr, full_word in abbreviations.items():
                        if re.search(rf"\b{abbr}\b", word, re.IGNORECASE):
                            word = re.sub(
                                rf"\b{abbr}\b", full_word, word, flags=re.IGNORECASE
                            )
                    try:
                        translated = ts.translate_text(
                            word, from_language="en", to_language="fr"
                        )
                        desc_fr += translated + " "
                    except Exception as e:
                        desc_fr += word + " "
                else:
                    desc_fr += word + " "  # If it's an integer, add it as is

            desc_fr = desc_fr.upper()

            # Define the pattern to match "(EN ANGLAIS SEULEMENT)"
            pattern = r"\(EN ANGLAIS SEULEMENT\)"

            # Use re.sub to replace the pattern with an empty string
            desc_fr = re.sub(pattern, "", desc_fr)

            if len(desc_fr) > chars - len(brand):
                while len(desc_fr) > chars - len(brand):
                    modified = False

                    desc_fr, modified = self.remove_chars(desc_fr)

                    if not modified:
                        break

            desc_fr = brand + desc_fr
            tree_result = [row["SKU"], desc, desc_fr]
            self.count += 1
            self.callback_function(tree_result)
            self.callback_row(self.count, self.total_rows)
            return desc_fr

    def shorten(self, row, chars, col_name, col_name_short):
        """
        This method was created after, it is triggered when the user presses the shorten button.
        It will read the file, load it into a dataframe. Call the remove_chars function to shorten,
        then it will update the excel file, and update the treeview using the callback function
        """

        if pd.isnull(row[col_name_short]):
            
            desc = row[col_name]

            words = desc.split()

            brand = words[0] + " "
            words = words[1:]

            desc_short = " ".join(words)
        
        

        while len(desc_short) > chars - len(brand):
            modified = False
            print(desc_short, len(desc_short))
            desc_short, modified = self.remove_chars(desc_short)

            if not modified:
                break
        
        return brand + desc_short
        

    def remove_chars(self, desc):
        """Remove chars method removes vowels and spaces from the translation. It goes from right to left.

        Args:
            desc (str): The translation to be shortened

        Returns:
            str: the shortened description
        """
        chars_to_remove = "AEIOUÀÂÉÈÊËÎÏÔÛÙÜ "

        modified = False

        for i in chars_to_remove:
            if i in desc:
                desc = desc[::-1].replace(i, "", 1)[::-1]
                modified = True

        return desc, modified
