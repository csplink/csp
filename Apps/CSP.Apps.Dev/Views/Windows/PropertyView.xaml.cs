using CSP.Events;
using Prism.Events;
using Prism.Ioc;
using Syncfusion.Windows.PropertyGrid;

namespace CSP.Apps.Dev.Views.Windows
{
    public partial class PropertyView
    {
        public PropertyView()
        {
            InitializeComponent();

            var containerExtension = ContainerLocator.Current;
            var eventAggregator = containerExtension.Resolve<IEventAggregator>();
            eventAggregator.GetEvent<PropertyEvent>().Subscribe(OnPropertyReceive);
            eventAggregator.GetEvent<CustomEditorEvent>().Subscribe(OnCustomEditorReceive);
        }

        private void OnCustomEditorReceive(CustomEditor editor)
        {
            Property.CustomEditorCollection.Add(editor);
        }

        private void OnPropertyReceive(object property)
        {
            Property.SelectedObject = property;
        }
    }
}