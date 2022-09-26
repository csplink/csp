using Prism.Mvvm;
using Syncfusion.Windows.PropertyGrid;
using System.ComponentModel;
using System.Reflection;
using System.Windows.Controls;
using System.Windows.Data;

namespace CSP.Components.ValuePropertyGrid
{
    public class StringEditor : BaseTypeEditor
    {
        private TextBox _textBox;

        public override void Attach(PropertyViewItem property, PropertyItem info) {
            if (info.Value is not StringEditorModel)
                return;

            var binding = new Binding("Value.String") {
                Mode = BindingMode.TwoWay,
                Source = info,
                UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
            };
            BindingOperations.SetBinding(_textBox, TextBox.TextProperty, binding);

            binding = new Binding("Value.String") {
                Mode = BindingMode.TwoWay,
                Source = info,
                UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
            };
            BindingOperations.SetBinding(_textBox, TextBox.ToolTipProperty, binding);

            _textBox.IsReadOnly = info.IsReadOnly;
        }

        public override object Create(PropertyInfo propertyInfo) {
            return CreateEditor();
        }

        public override object Create(PropertyDescriptor propertyDescriptor) {
            return CreateEditor();
        }

        public override void Detach(PropertyViewItem property) {
            _textBox = null;
        }

        private TextBox CreateEditor() {
            _textBox = new TextBox();
            return _textBox;
        }
    }

    public class StringEditorModel : BindableBase
    {
        private string _string = string.Empty;

        public string String {
            get => _string;
            set => SetProperty(ref _string, value);
        }
    }
}