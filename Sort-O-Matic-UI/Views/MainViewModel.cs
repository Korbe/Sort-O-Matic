using Sort_O_Matic_UI.Util;
using Sort_O_Matic_UI.Util.Gui;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows;
using System.Windows.Input;

namespace Sort_O_Matic_UI.Views
{
    public class MainViewModel : INotifyPropertyChanged
    {
        #region Member
        private RelayCommand selectSourceCommand = null;
        private RelayCommand selectTargetCommand = null;
        private RelayCommand executeCommand = null;

        public event PropertyChangedEventHandler PropertyChanged;

        private string sourcePath;
        private string targetPath;
        private bool isMove;
        #endregion

        public MainViewModel()
        {

        }

        public void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        #region Properties

        public string SourcePath
        {
            get { return sourcePath; }
            set
            {
                sourcePath = value;
                OnPropertyChanged(nameof(SourcePath));
            }
        }

        public string TargetPath
        {
            get { return targetPath; }
            set
            {
                targetPath = value;
                OnPropertyChanged(nameof(TargetPath));
            }
        }

        public bool IsMove
        {
            get { return isMove; }
            set
            {
                isMove = value;
                OnPropertyChanged(nameof(IsMove));
            }
        }


        #endregion

        #region commands

        public ICommand SelectSourceCommand
        {
            get
            {
                if (selectSourceCommand == null)
                    selectSourceCommand = new RelayCommand(
                        p => SourcePath = PathTools.SelectFolderDialog()
                    );

                return selectSourceCommand;
            }
        }

        public ICommand SelectTargetCommand
        {
            get
            {
                if (selectTargetCommand == null)
                    selectTargetCommand = new RelayCommand(
                        p => TargetPath = PathTools.SelectFolderDialog()
                    );

                return selectTargetCommand;
            }
        }

        public ICommand ExecuteCommand
        {
            get
            {
                if (executeCommand == null)
                    executeCommand = new RelayCommand(
                        p => Execute()
                    );

                return executeCommand;
            }
        }

        #endregion

        private void Execute()
        {
            var args = $@"py sort-o-matic.py -s ""{SourcePath}"" -t ""{TargetPath}""";
            if (IsMove)
            {
                args += " -m";
            }

            var startInfo = new System.Diagnostics.ProcessStartInfo
            {
                FileName = "cmd.exe",
                Arguments = $"/K {args}",
                UseShellExecute = true,
            };

            try
            {
                System.Diagnostics.Process.Start(startInfo);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Exception", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }
}
