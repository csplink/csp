using System;
using System.Globalization;
using System.Windows.Data;

namespace CSP.Utils.Converter;

public class IsNullConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture) {
        return value == null;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture) {
        DebugUtil.Assert(false, new InvalidOperationException("IsNullConverter can only be used OneWay."));

        return null;
    }
}