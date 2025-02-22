import wx 
import os
import subprocess

LOG_FILE = "log.txt"

def write_log(message):
    """ פונקציה לרישום הודעות ללוג """
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(message + "\n")
    print(message)  # גם מדפיס לקונסול לנוחות

class EncryptApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(EncryptApp, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox_file = wx.BoxSizer(wx.HORIZONTAL)
        self.file_text = wx.TextCtrl(panel, style=wx.TE_READONLY, size=(400, -1))
        browse_button = wx.Button(panel, label="Browse")
        browse_button.Bind(wx.EVT_BUTTON, self.OnBrowse)
        hbox_file.Add(self.file_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        hbox_file.Add(browse_button, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        self.serial_choice = wx.Choice(panel, size=(400, -1))
        self.UpdateUSBDevices()

        encrypt_button = wx.Button(panel, label="Encrypt")
        encrypt_button.Bind(wx.EVT_BUTTON, self.OnEncrypt)
        
        decrypt_button = wx.Button(panel, label="Decrypt")
        decrypt_button.Bind(wx.EVT_BUTTON, self.OnDecrypt)

        vbox.Add(hbox_file, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.serial_choice, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(encrypt_button, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(decrypt_button, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.SetTitle('CobaltEncrypter')
        self.SetSize((450, 300))
        self.Centre()

    def OnBrowse(self, event):
        dlg = wx.FileDialog(self, "Choose a file", wildcard="All files (*.*)|*.*", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.file_text.SetValue(dlg.GetPath())
        dlg.Destroy()

    def UpdateUSBDevices(self):
        devices = []
        command = "wmic logicaldisk where DriveType=2 get DeviceID, VolumeName"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        write_log("=== USB Device Detection ===")
        write_log(f"Command: {command}")
        write_log(f"WMIC Output:\n{stdout.decode()}")

        if process.returncode == 0:
            output = stdout.decode().strip().split("\n")[1:]  
            for line in output:
                parts = line.strip().split()
                if len(parts) == 2:
                    drive_letter, volume_name = parts
                    devices.append(f"{volume_name} ({drive_letter})")
                elif len(parts) == 1:
                    drive_letter = parts[0]
                    devices.append(f"Unknown ({drive_letter})")
        else:
            error_message = stderr.decode()
            write_log(f"Error detecting USB devices: {error_message}")
            wx.MessageBox(f"Error detecting USB devices: {error_message}", 'Error', wx.OK | wx.ICON_ERROR)

        self.serial_choice.Clear()
        if devices:
            self.serial_choice.AppendItems(devices)
        else:
            self.serial_choice.Append("No devices found.")
            wx.MessageBox('No USB device detected.', 'Error', wx.OK | wx.ICON_ERROR)

    def GetSerialNumber(self):
        serial = self.serial_choice.GetStringSelection()
        if not serial or serial == "No devices found.":
            wx.MessageBox('Please select a USB device.', 'Error', wx.OK | wx.ICON_ERROR)
            return None
        
        device_letter = serial.split(" (")[1].split(")")[0]
        command = f"wmic logicaldisk where DeviceID='{device_letter}' get VolumeSerialNumber"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            try:
                return stdout.decode().strip().split("\n")[1].strip()
            except IndexError:
                wx.MessageBox("Failed to retrieve volume serial number.", 'Error', wx.OK | wx.ICON_ERROR)
                return None
        else:
            error_message = stderr.decode()
            write_log(f"Error retrieving volume serial number: {error_message}")
            wx.MessageBox(f"Error: {error_message}", 'Error', wx.OK | wx.ICON_ERROR)
            return None

    def OnEncrypt(self, event):
        file_path = self.file_text.GetValue()
        if not file_path:
            wx.MessageBox('Please select a file to encrypt.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        serial_number = self.GetSerialNumber()
        if not serial_number:
            return

        encrypt_command = f'python sources/Encrypt.py {serial_number} "{file_path}"'
        process = subprocess.Popen(encrypt_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        write_log(f"Encrypt Output:\n{stdout.decode()}")
        
        if process.returncode == 0:
            wx.MessageBox('File encrypted successfully!', 'Success', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(f"Encryption failed: {stderr.decode()}", 'Error', wx.OK | wx.ICON_ERROR)

    def OnDecrypt(self, event):
        file_path = self.file_text.GetValue()
        if not file_path:
            wx.MessageBox('Please select a file to decrypt.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        serial_number = self.GetSerialNumber()
        if not serial_number:
            return

        decrypt_command = f'python sources/Decrypt.py {serial_number} "{file_path}"'
        process = subprocess.Popen(decrypt_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        write_log(f"Decrypt Output:\n{stdout.decode()}")
        
        if process.returncode == 0:
            wx.MessageBox('File decrypted successfully!', 'Success', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(f"Decryption failed: {stderr.decode()}", 'Error', wx.OK | wx.ICON_ERROR)


def main():
    app = wx.App(False)
    frame = EncryptApp(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
