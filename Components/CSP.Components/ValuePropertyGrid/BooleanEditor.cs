using System.ComponentModel;
using System.Reflection;
using System.Windows.Controls;
using System.Windows.Data;
using Prism.Mvvm;
using Syncfusion.Windows.PropertyGrid;

namespace CSP.Components.ValuePropertyGrid;

public class BooleanEditor : BaseTypeEditor
{
    private CheckBox _checkBox;

    public override void Attach(PropertyViewItem property, PropertyItem info) {
        if (info.Value is not BooleanEditorModel) {
            return;
        }

        Binding binding = new Binding("Value.Boolean") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_checkBox, CheckBox.IsCheckedProperty, binding);

        binding = new Binding("Value.Boolean") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_checkBox, CheckBox.ToolTipProperty, binding);

        _checkBox.IsEnabled = !info.IsReadOnly;
    }

    public override object Create(PropertyInfo propertyInfo) {
        return CreateEditor();
    }

    public override object Create(PropertyDescriptor propertyDescriptor) {
        return CreateEditor();
    }

    public override void Detach(PropertyViewItem property) {
        _checkBox = null;
    }

    private CheckBox CreateEditor() {
        _checkBox = new CheckBox();

        return _checkBox;
    }
}

public class BooleanEditorModel : BindableBase
{
    private bool _boolean;

    public bool Boolean {
        get => _boolean;
        set => SetProperty(ref _boolean, value);
    }
}