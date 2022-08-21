using System;

namespace CSP.Utils
{
    public static class DebugUtil
    {
        public static void Assert(bool condition, Exception exception, string message = "")
        {
#if DEBUG
            System.Diagnostics.Debug.Assert(condition, message, exception.ToString());
#else
            if(!condition)
            {
                Serilog.Log.Error(exception, message);
            }
#endif
        }
    }
}