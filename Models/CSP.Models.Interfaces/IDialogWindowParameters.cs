using Prism.Services.Dialogs;
using System.Windows;

namespace CSP.Models.Interfaces
{
    public interface IDialogWindowParameters : IDialogAware
    {
        public double Height { get; }
        public double MinHeight { get; }
        public double MinWidth { get; }
        public bool ShowInTaskbar { get; }
        public SizeToContent SizeToContent { get; }
        public double Width { get; }
        public WindowState WindowState { get; set; }
    }
}