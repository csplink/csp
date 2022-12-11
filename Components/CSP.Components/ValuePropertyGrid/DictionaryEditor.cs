using System.Collections.Generic;
using System.ComponentModel;
using System.Reflection;
using System.Windows.Controls;
using System.Windows.Data;
using CSP.Events;
using CSP.Utils;
using CSP.Utils.Extensions;
using Prism.Mvvm;
using Syncfusion.Windows.PropertyGrid;

namespace CSP.Components.ValuePropertyGrid;

public class DictionaryEditor : BaseTypeEditor
{
    private ComboBox _comboBox;

    public override void Attach(PropertyViewItem property, PropertyItem info) {
        if (info.Value is not DictionaryEditorModel value) {
            return;
        }

        Binding binding = new Binding("Value.Source") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_comboBox, ComboBox.ItemsSourceProperty, binding);

        binding = new Binding("Value.Value") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_comboBox, ComboBox.SelectedValueProperty, binding);

        binding = new Binding("Value.Value") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_comboBox, ComboBox.ToolTipProperty, binding);

        _comboBox.DisplayMemberPath = "Value";
        _comboBox.SelectedValuePath = "Key";

        if (value.Value.IsNullOrEmpty()) {
            _comboBox.SelectedIndex = 0;
        }
        else {
            _comboBox.SelectedValue = value.Value;
        }
    }

    public override object Create(PropertyInfo propertyInfo) {
        return CreateEditor();
    }

    public override object Create(PropertyDescriptor propertyDescriptor) {
        return CreateEditor();
    }

    public override void Detach(PropertyViewItem property) {
        _comboBox = null;
    }

    private ComboBox CreateEditor() {
        _comboBox = new ComboBox();

        return _comboBox;
    }
}

public class DictionaryEditorModel : BindableBase
{
    private string _value;

    public ObservableDictionary<string, string> Source { get; init; } = new();

    public string Value {
        get => _value;
        set {
            if (EqualityComparer<string>.Default.Equals(_value, value)) {
                return;
            }

            PropertyValueChanged?.Invoke(this, new PropertyValueChangedEventArgs("Value", _value, value));
            SetProperty(ref _value, value);
        }
    }

    public event PropertyValueChangedEventHandler PropertyValueChanged;
}