#include "foreign_library.h"
#include <liballocs.h>

static PyObject *allocs_get_type(PyObject *self, PyObject *obj)
{
    struct uniqtype *t = __liballocs_get_alloc_type(obj);
    if (!t) Py_RETURN_NONE;

    return PyUnicode_FromString(__liballocs_uniqtype_name(t));
}

static PyMethodDef AllocsMethods[] =
{
    {"get_type", allocs_get_type, METH_O, "Lookup type information gathered by liballocs."},
    {NULL, NULL, 0, NULL}   /* Sentinel */
};

static struct PyModuleDef allocsmodule =
{
    PyModuleDef_HEAD_INIT,
    "allocs",   /* name of module */
    NULL,       /* module documentation, may be NULL */
    -1,         /* size of per-interpreter state of the module,
                   or -1 if the module keeps state in global variables. */
    AllocsMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_allocs(void)
{
    if (PyType_Ready(&ForeignLibraryLoader_Type) < 0) return NULL;
    if (PyType_Ready(&ForeignProxy_Type) < 0) return NULL;
    if (PyType_Ready(&ForeignType_Type) < 0) return NULL;
    if (PyType_Ready(&ForeignFunction_ProxyMetatype) < 0) return NULL;
    if (PyType_Ready(&ForeignComposite_ProxyMetatype) < 0) return NULL;
    if (PyType_Ready(&ForeignAddress_ProxyMetatype) < 0) return NULL;

    PyObject *m = PyModule_Create(&allocsmodule);
    if (m == NULL) return NULL;

    Py_INCREF(&ForeignLibraryLoader_Type);
    PyModule_AddObject(m, "ForeignLibraryLoader", (PyObject *) &ForeignLibraryLoader_Type);
    Py_INCREF(&ForeignProxy_Type);
    PyModule_AddObject(m, "ForeignProxy", (PyObject *) &ForeignProxy_Type);
    Py_INCREF(&ForeignType_Type);
    PyModule_AddObject(m, "ForeignType", (PyObject *) &ForeignType_Type);
    Py_INCREF(&ForeignFunction_ProxyMetatype);
    PyModule_AddObject(m, "ForeignFunctionProxyType", (PyObject *) &ForeignFunction_ProxyMetatype);
    Py_INCREF(&ForeignComposite_ProxyMetatype);
    PyModule_AddObject(m, "ForeignCompositeProxyMetatype", (PyObject *) &ForeignComposite_ProxyMetatype);
    Py_INCREF(&ForeignAddress_ProxyMetatype);
    PyModule_AddObject(m, "ForeignAddressProxyMetatype", (PyObject *) &ForeignAddress_ProxyMetatype);

    return m;
}
