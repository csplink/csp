using System.ComponentModel;

namespace CSP.Events
{
    public delegate void PropertyValueChangedEventHandler(object sender, PropertyValueChangedEventArgs e);

    public class PropertyValueChangedEventArgs : PropertyChangedEventArgs
    {
        public PropertyValueChangedEventArgs(string propertyName) : base(propertyName) {
        }

        public PropertyValueChangedEventArgs(string propertyName, object oldValue, object newValue) : base(propertyName) {
            NewValue = newValue;
            OldValue = oldValue;
        }

        public virtual object NewValue { get; }
        public virtual object OldValue { get; }
    }
}