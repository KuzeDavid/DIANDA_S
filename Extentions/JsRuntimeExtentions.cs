using Microsoft.JSInterop;
using System.Threading.Tasks;

namespace BlazorServerAppCorreoPrueba.Extentions
{
    public static class JsRuntimeExtentions
    {
        public static ValueTask ToastrSuccess(this IJSRuntime jSRuntime, string message)
        {
            return jSRuntime.InvokeVoidAsync("ShowToastr", "success", message);
        }
        //for error message of an opration
        public static ValueTask ToastrError(this IJSRuntime jsSRuntime, string message)
        {
            return jsSRuntime.InvokeVoidAsync("ShowToastr", "error", message);
        }
    }
}
