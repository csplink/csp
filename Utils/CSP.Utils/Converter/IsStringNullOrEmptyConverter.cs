using System;
using System.Globalization;
using System.Windows.Data;
using CSP.Utils.Extensions;

namespace CSP.Utils.Converter
{
    public class IsStringNullOrEmptyConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture) {
            if (value is string str)
                return str.IsNullOrEmpty();

            throw new ArgumentException("IsStringNullOrEmptyConverter can only be used String");
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture) {
            throw new InvalidOperationException("IsStringNullOrEmptyConverter can only be used OneWay.");
        }
    }
}