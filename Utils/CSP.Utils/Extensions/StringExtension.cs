using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace CSP.Utils.Extensions
{
    public static class StringExtension
    {
        public static byte[] FromHexToByteArray(this string str)
        {
            if (str == null)
                throw new ArgumentNullException(nameof(str));

            var chars = str.Replace(" ", "").Split(2);
            var returnBytes = new byte[chars.Length];

            //逐个字符变为16进制字节数据
            for (var i = 0; i < chars.Length; i++)
                returnBytes[i] = Convert.ToByte(chars[i], 16);

            return returnBytes;
        }

        public static string FromHexToText(this string str, Encoding encoding)
        {
            if (str == null)
                throw new ArgumentNullException(nameof(str));
            if (encoding == null)
                throw new ArgumentNullException(nameof(encoding));

            var bytes = str.FromHexToByteArray();
            return encoding.GetString(bytes);
        }

        public static byte[] FromTextToByteArray(this string str, Encoding encoding)
        {
            if (str == null)
                throw new ArgumentNullException(nameof(str));
            if (encoding == null)
                throw new ArgumentNullException(nameof(encoding));

            return encoding.GetBytes(str);
        }

        public static string FromTextToHex(this string str, Encoding encoding)
        {
            if (str == null)
                throw new ArgumentNullException(nameof(str));
            if (encoding == null)
                throw new ArgumentNullException(nameof(encoding));

            return BitConverter.ToString(encoding.GetBytes(str)).Replace("-", " ");
        }

        public static bool IsLegalHex(this string str)
        {
            if (str == null)
                throw new ArgumentNullException(nameof(str));

            IList<char> hexSet = new List<char>
                { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f' };

            return str.All(item => hexSet.Contains<char>(item));
        }

        public static bool IsNullOrEmpty(this string s)
        {
            return string.IsNullOrEmpty(s);
        }

        /// <summary>
        /// 按指定长度分割字符串
        /// </summary>
        /// <param name="str">
        /// 原字符串
        /// </param>
        /// <param name="count">
        /// 分割长度
        /// </param>
        /// <returns>
        /// 被分割后的字符串
        /// </returns>
        public static string[] Split(this string str, int count)
        {
            if (str == null)
                throw new ArgumentNullException(nameof(str));

            List<string> list = new();

            for (var i = 0; i < str.Length; i += count)
                list.Add((str.Length - i) > count ? str.Substring(i, count) : str.Substring(i));

            return list.ToArray();
        }
    }
}