using Prism.Mvvm;
using Syncfusion.Windows.PropertyGrid;

namespace CSP.Apps.Dev.ViewModels.Windows
{
    public class PropertyViewModel : BindableBase
    {
        private CustomEditorCollection _customEditorCollection = new();
        private object _selectedObject;

        public PropertyViewModel() {
        }

        public CustomEditorCollection CustomEditorCollection {
            get => _customEditorCollection;
            set => SetProperty(ref _customEditorCollection, value);
        }

        public object SelectedObject {
            get => _selectedObject;
            set => SetProperty(ref _selectedObject, value);
        }
    }
}