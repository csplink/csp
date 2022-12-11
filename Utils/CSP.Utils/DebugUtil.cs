using System;
using System.Diagnostics;

namespace CSP.Utils;

public static class DebugUtil
{
    public static void Assert(bool condition, Exception exception, string message = "") {
#if DEBUG
        Debug.Assert(condition, message, exception.ToString());
#else
        if(!condition)
        {
            Serilog.Log.Error(exception, message);
        }
#endif
    }
}