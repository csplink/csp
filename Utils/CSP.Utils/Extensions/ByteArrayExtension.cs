using System;
using System.Text;

namespace CSP.Utils.Extensions;

public static class ByteArrayExtension
{
    public static string FromHexToString(this byte[] bytes) {
        StringBuilder builder = new StringBuilder();

        foreach (byte t in bytes) {
            builder.Append($"{t:X2} ");
        }

        return builder.ToString().Trim();
    }

    public static string FromTextToString(this byte[] bytes, Encoding encoding) {
        if (bytes == null) {
            throw new ArgumentNullException(nameof(bytes));
        }

        if (encoding == null) {
            throw new ArgumentNullException(nameof(encoding));
        }

        return encoding.GetString(bytes);
    }
}