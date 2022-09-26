using CSP.Utils;
using Prism.Events;
using Prism.Mvvm;
using System;
using System.Collections;
using System.ComponentModel;
using System.Linq;

namespace CSP.Events
{
    public class CustomPropertyDescriptor : PropertyDescriptor
    {
        private readonly PropertyDetails _propertyDetails;

        #region Constructors

        public CustomPropertyDescriptor(PropertyDetails propertyDetails,
                                        string propertyName,
                                        string propertyDisplayName,
                                        Type propertyType,
                                        Attribute[] propertyAttributes)
            : base(propertyName, propertyAttributes) {
            this._propertyDetails = propertyDetails;
            PropertyType = propertyType;
            DisplayName = propertyDisplayName;
        }

        #endregion Constructors

        #region Properties

        public override Type ComponentType {
            get => typeof(PropertyDetails);
        }

        public override string DisplayName { get; }

        public override bool IsReadOnly {
            get => false;
        }

        public override Type PropertyType { get; }

        #endregion Properties

        #region Override members

        public override bool CanResetValue(object component) {
            return true;
        }

        public override object GetValue(object component) {
            return _propertyDetails.Details[base.Name];
        }

        public override void ResetValue(object component) {
        }

        public override void SetValue(object component, object value) {
            _propertyDetails.Details[Name] = value;
        }

        public override bool ShouldSerializeValue(object component) {
            return false;
        }

        #endregion Override members
    }

    public class PropertyDetails : BindableBase, ICustomTypeDescriptor
    {
        private ObservableDictionary<string, ObservableDictionary<string, Attribute>> _attributes = new();
        private ObservableDictionary<string, object> _details = new();

        #region Properties

        public ObservableDictionary<string, ObservableDictionary<string, Attribute>> Attributes {
            get => _attributes;
            set => SetProperty(ref _attributes, value);
        }

        public ObservableDictionary<string, object> Details {
            get { return _details; }
            set => SetProperty(ref _details, value);
        }

        #endregion Properties

        #region ICustomTypeDescriptor Members

        public AttributeCollection GetAttributes() {
            return TypeDescriptor.GetAttributes(this, true);
        }

        public string GetClassName() {
            return TypeDescriptor.GetClassName(this, true);
        }

        public string GetComponentName() {
            return TypeDescriptor.GetComponentName(this, true);
        }

        public TypeConverter GetConverter() {
            return TypeDescriptor.GetConverter(this, true);
        }

        public EventDescriptor GetDefaultEvent() {
            return TypeDescriptor.GetDefaultEvent(this, true);
        }

        public PropertyDescriptor GetDefaultProperty() {
            return TypeDescriptor.GetDefaultProperty(this, true);
        }

        public object GetEditor(Type editorBaseType) {
            return TypeDescriptor.GetEditor(this, editorBaseType, true);
        }

        public EventDescriptorCollection GetEvents() {
            return TypeDescriptor.GetEvents(this, true);
        }

        public EventDescriptorCollection GetEvents(Attribute[] attributes) {
            return TypeDescriptor.GetEvents(this, attributes, true);
        }

        public PropertyDescriptorCollection GetProperties() {
            var details = Details.Select(element => {
                Attributes.TryGetValue(element.Key, out var attributes);
                attributes ??= new ObservableDictionary<string, Attribute> { { "DisplayName", new DisplayNameAttribute(element.Key) } };
                return new CustomPropertyDescriptor(this,
                                                    element.Key,
                                                    ((DisplayNameAttribute)attributes["DisplayName"]).DisplayName,
                                                    element.Value.GetType(),
                                                    attributes.Values.ToArray());
            });
            // ReSharper disable once CoVariantArrayConversion
            return new PropertyDescriptorCollection(details.ToArray());
        }

        public PropertyDescriptorCollection GetProperties(Attribute[] attributes) {
            // ReSharper disable once CollectionNeverUpdated.Local
            ArrayList list = new();
            var propCollection = (PropertyDescriptor[])list.ToArray(typeof(PropertyDescriptor));
            return new PropertyDescriptorCollection(propCollection);
        }

        public object GetPropertyOwner(PropertyDescriptor pd) {
            return this;
        }

        #endregion ICustomTypeDescriptor Members
    }

    public class PropertyEvent : PubSubEvent<object>
    {
    }
}