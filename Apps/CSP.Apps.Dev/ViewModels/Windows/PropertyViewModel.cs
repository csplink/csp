using CSP.Components.ValuePropertyGrid;
using CSP.Events;
using Prism.Events;
using Prism.Mvvm;
using Syncfusion.Windows.PropertyGrid;

namespace CSP.Apps.Dev.ViewModels.Windows
{
    public class PropertyViewModel : BindableBase
    {
        private readonly IEventAggregator _eventAggregator;

        public PropertyViewModel(IEventAggregator eventAggregator) {
            _eventAggregator = eventAggregator;

            eventAggregator.GetEvent<RenderedEvent>().Subscribe(name => {
                AddCustomEditor();
            });
        }

        private void AddCustomEditor() {
            CustomEditor editor = new() {
                Editor = new DictionaryEditor(),
                HasPropertyType = true,
                PropertyType = typeof(DictionaryEditorModel)
            };
            _eventAggregator.GetEvent<CustomEditorEvent>().Publish(editor);

            editor = new CustomEditor {
                Editor = new StringEditor(),
                HasPropertyType = true,
                PropertyType = typeof(StringEditorModel)
            };
            _eventAggregator.GetEvent<CustomEditorEvent>().Publish(editor);

            editor = new CustomEditor {
                Editor = new BooleanEditor(),
                HasPropertyType = true,
                PropertyType = typeof(BooleanEditorModel)
            };
            _eventAggregator.GetEvent<CustomEditorEvent>().Publish(editor);
        }
    }
}