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

        private void OnPropertyReceive(PropertyEvent.Model model)
        {
            if (model.ShowList != null)
            {
                Property.HidePropertiesCollection.Clear();
                var properties = model.Data.GetType().GetProperties();
                foreach (var info in properties)
                {
                    if (!model.ShowList.Contains(info.Name))
                    {
                        Property.HidePropertiesCollection.Add(info.Name);
                    }
                }
            }

            Property.SelectedObject = model.Data;
        }
    }
}