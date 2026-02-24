using Microsoft.Win32;

namespace Sort_O_Matic_UI.Util
{
    public class PathTools
    {
        public static string SelectFolderDialog()
        {
            OpenFolderDialog openFolderDialog = new OpenFolderDialog()
            {
                Title = "Select folder to open ...",
                InitialDirectory = AppDomain.CurrentDomain.BaseDirectory
            };

            if (openFolderDialog.ShowDialog() == true)
                return openFolderDialog.FolderName;
            return null;
        }
    }
}