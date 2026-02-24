using Sort_O_Matic_UI.Views;
using System.Windows;

namespace Sort_O_Matic_UI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        readonly MainViewModel mainViewModel;

        public MainWindow()
        {
            InitializeComponent();

            this.mainViewModel = new MainViewModel();
            base.DataContext = mainViewModel;
        }
    }
}