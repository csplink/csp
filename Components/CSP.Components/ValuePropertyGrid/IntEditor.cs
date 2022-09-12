using Prism.Mvvm;
using Syncfusion.Windows.PropertyGrid;
using Syncfusion.Windows.Shared;
using System.ComponentModel;
using System.Reflection;
using System.Windows.Data;

namespace CSP.Components.ValuePropertyGrid
{
    public class IntEditor : BaseTypeEditor
    {
        private IntegerTextBox _integerTextBox;

        public override void Attach(PropertyViewItem property, PropertyItem info) {
            if (info.Value is not IntEditorModel)
                return;

            var binding = new Binding("Value.Boolean") {
                Mode = BindingMode.TwoWay,
                Source = info,
                UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
            };
            BindingOperations.SetBinding(_integerTextBox, IntegerTextBox.ValueProperty, binding);

            binding = new Binding("Value.Boolean") {
                Mode = BindingMode.TwoWay,
                Source = info,
                UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
            };
            BindingOperations.SetBinding(_integerTextBox, IntegerTextBox.ToolTipProperty, binding);

            _integerTextBox.IsReadOnly = info.IsReadOnly;
        }

        public override object Create(PropertyInfo propertyInfo) {
            return CreateEditor();
        }

        public override object Create(PropertyDescriptor propertyDescriptor) {
            return CreateEditor();
        }

        public override void Detach(PropertyViewItem property) {
            _integerTextBox = null;
        }

        private IntegerTextBox CreateEditor() {
            _integerTextBox = new IntegerTextBox();
            return _integerTextBox;
        }
    }

    public class IntEditorModel : BindableBase
    {
        private int _int;

        public int Int {
            get => _int;
            set => SetProperty(ref _int, value);
        }
    }
}