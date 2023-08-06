import time
from enum import Enum
from dateutil import parser
import datetime
from typing import Dict, List, Generic, TypeVar
import tkinter
import tkinter.filedialog as fd
from coopui.IAtomicUserInteraction import IAtomicUserInteraction
from pprint import pprint
import pandas as pd

T = TypeVar('T')

class CliAtomicUserInteraction(IAtomicUserInteraction):

    def __init__(self):
        pass

    def notify_user(self, text: str):
        print(text)
        time.sleep(1)

    def request_string(self, prompt: str, default:str = None):
        if default:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"(enter for default [{default}]):"

        inp = input(prompt).strip()

        if len(inp) == 0 and default:
            return default
        else:
            return inp

    def request_int(self, prompt: str, min: int = None, max: int = None):

        if min and max:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[between {min} and {max}]:"
        elif min:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[greater than {min}]:"
        elif max:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[less than {max}]:"

        while True:
            try:
                ret = input(prompt)

                if ret in ("X", "", None):
                    self.notify_user("Cancel...")
                    return None

                ret = int(ret)

                if min and ret < min:
                    raise Exception(f"Must be a greater than {min}")

                if max and ret > max:
                    raise Exception(f"Must be a less than {max}")

                if ret:
                    return ret
            except Exception as e:
                self.notify_user(f"Invalid Integer entry: {e}")

    def request_enum(self, enum, prompt:str=None):
        if prompt is None:
            prompt = f"Enter {enum.__name__}:"

        while True:
            if issubclass(enum, Enum):
                print(prompt)
                for i in enum:
                    print(f"{i.value} -- {i.name}")
                inp = input("")

                enum_num = self.int_tryParse(inp)
                if enum_num and enum.has_value(enum_num):
                    return enum(enum_num).name
                elif not enum_num and enum.has_name(inp):
                    return inp
                else:
                    print(f"Invalid Entry...")

            else:
                raise TypeError(f"Input must be of type Enum but {type(enum)} was provided")

    def request_float(self, prompt: str, min: float = None, max: float = None):
        if min and max:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[between {min} and {max}]:"
        elif min:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[greater than {min}]:"
        elif max:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[less than {max}]:"

        while True:
            try:
                ret = input(prompt)

                if ret in ("X", "", None):
                    self.notify_user("Cancel...")
                    return None

                inp = float(ret)
                if min and inp < min:
                    raise Exception(f"Must be a greater than {min}")

                if max and inp > max:
                    raise Exception(f"Must be a less than {max}")

                return inp
            except Exception as e:
                self.notify_user(f"invalid float entry: {e}")

    def request_guid(self, prompt: str):
        while True:
            inp = input(prompt)
            if (len(inp)) == 24:
                return inp
            else:
                self.notify_user("Invalid Guid...")

    def request_date(self, prompt: str = None):
        if prompt is None:
            prompt = "Date"

        prompt.replace(":", "")

        while True:
            inp = input(f"{prompt} (Blank for current date):")
            try:
                if inp == '':
                    date_stamp = datetime.datetime.now()
                    print(f"using: {date_stamp}")
                else:
                    date_stamp = parser.parse(inp)
                break
            except:
                print("invalid date format")

        return date_stamp

    def request_from_list(self, selectionList: List[T], prompt=None, cancel_text: str = 'CANCEL SELECTION') -> T:
        ret = self.request_from_dict({ii: item for ii, item in enumerate(selectionList)}, prompt, cancel_text)
        if ret is None:
            return ret

        return selectionList[ret]

    def request_from_objects(self, selectionList: List[T], objectIdentifier: str, prompt=None, cancel_text: str = 'CANCEL SELECTION') -> T:
        item_id = self.request_from_list([str(vars(obj)[objectIdentifier]) for obj in selectionList], prompt=prompt, cancel_text=cancel_text)
        if item_id is None:
            return item_id

        return next(item for item in selectionList if str(vars(item)[objectIdentifier]) == item_id)

    def request_from_dict(self, selectionDict: Dict[int, str], prompt=None, cancel_text: str = 'CANCEL SELECTION') -> int:
        if prompt is None:
            prompt = ""

        cancel = 'X'

        while True:
            print(prompt)
            for key in selectionDict:
                print(f"{key} -- {selectionDict[key]}")

            if cancel_text is not None:
                print(f"{cancel} -- {cancel_text}")

            inp = input("").upper()
            if cancel_text is not None and inp == cancel:
                return None

            inp = self.int_tryParse(inp)

            if (inp or type(inp) == int) and selectionDict.get(inp, None) is not None:
                return inp
            else:
                print("Invalid Entry...")

    def request_index_from_df(self, df: pd.DataFrame, prompt: str = None, cancel_text: str = 'CANCEL SELECTION'):
        if prompt is None:
            prompt = ""

        cancel = 'X'

        while True:
            self.pretty_print_dataframe(df, prompt)

            if cancel_text is not None:
                print(f"{cancel} -- {cancel_text}")

            inp = input("").upper()
            if cancel_text is not None and inp == cancel:
                return None

            if (int(inp) in df.index):
                return int(inp)
            else:
                print("Invalid Entry...")


    def request_open_filepath(self):
        root = tkinter.Tk()
        in_path = fd.askopenfilename()
        root.destroy()

        return in_path

    def request_save_filepath(self):
        root = tkinter.Tk()
        in_path = fd.asksaveasfilename()
        root.destroy()

        return in_path

    def request_you_sure(self, items, prompt=None, cancel_text: str = 'CANCEL SELECTION'):
        return self.request_from_dict({1: "Yes", 2: "No"}, prompt, cancel_text=cancel_text)

    def request_bool(self, prompt=None, cancel_text: str = 'CANCEL SELECTION'):
        ret = self.request_from_dict({1: "True", 2: "False"}, prompt, cancel_text=cancel_text)
        if ret == 1:
            return True
        elif ret == 2:
            return False
        elif ret is None:
            return None
        else:
            raise NotImplementedError(f"Unhandled return [{ret}] from request_from_dict")

    def request_yes_no(self, prompt:str=None, cancel_text: str = 'CANCEL SELECTION') -> bool:
        ret = self.request_from_dict({1: "Yes", 2: "No"}, prompt, cancel_text=cancel_text)

        if ret == 1:
            return True
        elif ret == 2:
            return False
        elif ret is None:
            return None
        else:
            raise NotImplementedError(f"Unhandled return [{ret}] from request_from_dict")

    def float_as_currency(self, val: float):
        return "${:,.2f}".format(round(val, 2))

    def int_tryParse(self, value):
        try:
            return int(value)
        except:
            return False

    def pprint_items(self, items, header:str=None):
        if header:
            print(header)
        pprint(items)

    @staticmethod
    def pretty_print_dataframe(df: pd.DataFrame, title: str = None):
        if title:
            print(title)

        with pd.option_context('display.max_rows', 500, 'display.max_columns', 2000, 'display.width', 250):
            print(f"{df}\n")
