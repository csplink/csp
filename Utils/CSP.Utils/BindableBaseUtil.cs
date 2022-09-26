using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace CSP.Utils
{
    public delegate void PropertyValueChangedEventHandler(object sender, PropertyValueChangedEventArgs e);

    public abstract class BindableBaseUtil : BindableBase
    {
        public new event PropertyChangedEventHandler PropertyChanged;

        public event PropertyValueChangedEventHandler PropertyValueChanged;

        protected override void OnPropertyChanged(PropertyChangedEventArgs args) {
            PropertyChanged?.Invoke(this, args);
        }

        protected new void RaisePropertyChanged([CallerMemberName] string propertyName = null) {
            OnPropertyChanged(new PropertyChangedEventArgs(propertyName));
        }

        protected override bool SetProperty<T>(ref T storage, T value, [CallerMemberName] string propertyName = null) {
            if (EqualityComparer<T>.Default.Equals(storage, value)) return false;
            PropertyValueChanged?.Invoke(this, new PropertyValueChangedEventArgs(propertyName, storage, value));
            storage = value;
            RaisePropertyChanged(propertyName);

            return true;
        }

        protected override bool SetProperty<T>(ref T storage, T value, Action onChanged, [CallerMemberName] string propertyName = null) {
            if (EqualityComparer<T>.Default.Equals(storage, value)) return false;
            PropertyValueChanged?.Invoke(this, new PropertyValueChangedEventArgs(propertyName, storage, value));
            storage = value;
            onChanged?.Invoke();
            RaisePropertyChanged(propertyName);

            return true;
        }
    }

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