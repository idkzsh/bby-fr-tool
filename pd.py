import pandas as pd
import translators as ts
import re
import time

# _ = ts.preaccelerate_and_speedtest()


class BBYTranslator:
    def __init__(self):
        pass

    # translate the whole sku
    def translate_sku(row, column_name_fr, column_name, chars):
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
            print(f"===========ENGLISH: {desc}===========")

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
            print(desc_fr)

            if len(desc_fr) > chars - len(brand):
                while len(desc_fr) > chars - len(brand):
                    print(desc_fr)
                    modified = False

                    desc_fr, modified = remove_chars(desc_fr)

                    if not modified:
                        break

            desc_fr = brand + desc_fr
            # desc_fr = re.sub(r'\s+', ' ', desc_fr).strip()

            return desc_fr

    # translate word by word
    def translate_word(row, column_name_fr, column_name, chars):
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
            print(f"===========ENGLISH: {desc}===========")

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
            print(desc_fr)

            if len(desc_fr) > chars - len(brand):
                while len(desc_fr) > chars - len(brand):
                    print(desc_fr)
                    modified = False

                    desc_fr, modified = remove_chars(desc_fr)

                    if not modified:
                        break

            desc_fr = brand + desc_fr

            return desc_fr

    def remove_chars(desc):
        # Define the set of vowels to remove
        chars_to_remove = "AEIOUÀÂÉÈÊËÎÏÔÛÙÜ "

        modified = False

        for i in chars_to_remove:
            if i in desc:
                desc = desc[::-1].replace(i, "", 1)[::-1]
                modified = True

        return desc, modified

def main():
    # input_file = "french_data_test.xlsx"

    # # Load the Excel file into a DataFrame
    # df = pd.read_excel(input_file)

    # # start the timer
    # start_time = time.time()

    # # Apply the translation function to each row in the DataFrame
    # df["SKU_DESC FRENCH"] = df.apply(
    #     translate_to_french,
    #     column_name_fr="SKU_DESC FRENCH",
    #     column_name="SKU_DESC",
    #     chars=40,
    #     axis=1,
    # )
    # df["SHORT_DESC FRENCH"] = df.apply(
    #     translate_to_french,
    #     column_name_fr="SHORT_DESC FRENCH",
    #     column_name="SHORT_DESC",
    #     chars=20,
    #     axis=1,
    # )
    # # end the timer
    # end_time = time.time()

    # elapsed_time = end_time - start_time

    # # Save the DataFrame with translations to a new Excel file
    # output_file = "translated_data.xlsx"
    # df.to_excel(output_file, index=False)

    # print(f"Data with translations saved to {output_file}")
    # print(f"Execution time: {elapsed_time:.2f} seconds")
    pass





if __name__ == "__main__":
    main()
