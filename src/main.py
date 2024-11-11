import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
from collections import defaultdict
import xml.etree.ElementTree as ET


class XMLParserModel:
    def __init__(self):
        self.parts_data = defaultdict(
            lambda: {"description": "", "amount": 0, "value_per_unit": None}
        )

    def parse_xml(self, input_path: str) -> str:
        """Parse the input XML file and returns vin.

        Args:
            input_path (str): Path to the input XML file.

        Returns:
            str: VIN number.
        """
        with open(input_path, "r") as f:
            data = f.read()

        namespace = {"ns": "http://www.dat.de/vxs"}
        root = ET.fromstring(data)

        vin = root.find(".//ns:VehicleIdentNumber", namespaces=namespace).text

        for repair_position in root.findall(
            ".//ns:MaterialPosition", namespaces=namespace
        ):
            part_number_elem = repair_position.find(
                "ns:PartNumber", namespaces=namespace
            )
            description = repair_position.find("ns:Description", namespaces=namespace)
            amount = repair_position.find("ns:Amount", namespaces=namespace)
            value_per_unit = repair_position.find(
                "ns:ValuePerUnit", namespaces=namespace
            )

            if (
                part_number_elem is not None
                and amount is not None
                and value_per_unit is not None
            ):
                part_number = part_number_elem.text
                self.parts_data[part_number]["description"] = description.text
                self.parts_data[part_number]["amount"] += float(amount.text)
                temp = float(value_per_unit.text)
                curr = self.parts_data[part_number]["value_per_unit"]
                if curr is not None and temp != curr:
                    print(
                        f"Value per unit changed from {curr} to {temp} for part number {part_number}"
                    )
                self.parts_data[part_number]["value_per_unit"] = float(
                    value_per_unit.text
                )
                self.parts_data[part_number]["total_price"] = (
                    self.parts_data[part_number]["amount"]
                    * self.parts_data[part_number]["value_per_unit"]
                )

        return vin

    def save_to_csv(self, vin, output_path):
        df = pd.DataFrame(self.parts_data).T
        df["Typ"] = "TNR"
        df["TG"] = None
        df = df.reset_index()
        df.columns = [
            "Teilenummer",
            "Beschreibung",
            "Menge",
            "UPE",
            "Gesamtpreis",
            "Typ",
            "TG",
        ]

        df.loc[-1] = [vin, None, None, None, None, "TEXT", None]
        df = df.sort_index()
        df = df.reset_index()
        df = df.rename(columns={"index": "Pos."})
        df["Pos."] = df["Pos."] + 2

        df = df[
            [
                "Pos.",
                "Typ",
                "Teilenummer",
                "Beschreibung",
                "TG",
                "UPE",
                "Menge",
                "Gesamtpreis",
            ]
        ]
        df["UPE"] = df["UPE"].round(2)
        df = df.astype({"Gesamtpreis": np.float64, "UPE": np.float64, "TG": np.float64})

        df.to_csv(output_path, index=False, sep=";", columns=df.columns, decimal=",")


class XMLParserView:
    def __init__(self, root):
        self.root = root
        self.root.title("XML-to-CSV Parser")

        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Input XML File:").grid(
            row=0, column=0, padx=10, pady=10
        )
        tk.Entry(self.root, textvariable=self.input_file_path, width=50).grid(
            row=0, column=1, padx=10, pady=10
        )
        tk.Button(self.root, text="Browse", command=self.browse_input_file).grid(
            row=0, column=2, padx=10, pady=10
        )

        tk.Label(self.root, text="Select Output CSV File:").grid(
            row=1, column=0, padx=10, pady=10
        )
        tk.Entry(self.root, textvariable=self.output_file_path, width=50).grid(
            row=1, column=1, padx=10, pady=10
        )
        tk.Button(self.root, text="Browse", command=self.browse_output_file).grid(
            row=1, column=2, padx=10, pady=10
        )

        tk.Button(
            self.root, text="Parse and Validate", command=self.parse_and_validate
        ).grid(row=2, column=0, columnspan=3, pady=20)

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("All files", "*.*"), ("XML files", "*.xml")]
        )
        if file_path:
            self.input_file_path.set(file_path)

        if os.path.splitext(file_path)[-1].lower() != ".xml":
            messagebox.showwarning("Warning", "You are trying to parse a non-XML file.")

    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            self.output_file_path.set(file_path)

    def parse_and_validate(self):
        self.controller.parse_and_validate()

    def set_controller(self, controller):
        self.controller = controller


class XMLParserController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def parse_and_validate(self):
        input_path = self.view.input_file_path.get()
        output_path = self.view.output_file_path.get()

        if not input_path or not output_path:
            messagebox.showerror("Error", "Please select both input and output files.")
            return
        elif input_path == output_path:
            messagebox.showerror(
                "Error",
                "Input and output files cannot be the same. Please select different files.",
            )
            return
        elif not os.path.exists(input_path):
            messagebox.showerror("Error", "Input file does not exist.")
            return

        try:
            vin = self.model.parse_xml(input_path)
            self.model.save_to_csv(vin, output_path)
            messagebox.showinfo(
                "Success",
                f"File [{input_path.split(os.sep)[-1]}] parsed and saved successfully and saved to {output_path.split(os.sep)[-1]}",
            )
            self.view.input_file_path.set("")
            self.view.output_file_path.set("")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    model = XMLParserModel()
    view = XMLParserView(root)
    controller = XMLParserController(model, view)
    root.mainloop()
