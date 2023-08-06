#include "Python.h"
#include "fasta.h"
#include "fastq.h"
#include "fastx.h"
#include "util.h"
#include "read.h"
#include "sequence.h"
#include "fakeys.h"
#include "fqkeys.h"
#include "version.h"
#include "sqlite3.h"
#include "zlib.h"

PyObject *pyfastx_version(PyObject *self, PyObject *args, PyObject *kwargs)	{
	int debug = 0;

	static char* keywords[] = {"debug", NULL};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|i", keywords, &debug)) {
		return NULL;
	}

	if (debug) {
		return PyUnicode_FromFormat("pyfastx: %s; zlib: %s; sqlite: %s; zran: %s", PYFASTX_VERSION, ZLIB_VERSION, SQLITE_VERSION, ZRAN_VERSION);
	}

	return Py_BuildValue("s", PYFASTX_VERSION);
}

PyObject *pyfastx_gzip_check(PyObject *self, PyObject *args) {
	char *file_name;

	if (!PyArg_ParseTuple(args, "s", &file_name)) {
		return NULL;
	}

	if (is_gzip_format(file_name)) {
		Py_RETURN_TRUE;
	}

	Py_RETURN_FALSE;
}

/*PyObject *pyfastx_test(PyObject *self) {
	PyObject *result;
	char *hello = "hello, world";
	result = PyUnicode_New(strlen(hello), 127);

	if (result == NULL)
		return NULL;

	//Py_USC1 *data = PyUnicode_1BYTE_DATA(result);

	memcpy(PyUnicode_1BYTE_DATA(result), hello, strlen(hello));
	return result;
	char *s = (char *)malloc(1);
	s[0] = '\0';
	return Py_BuildValue("s", s);
}*/

static PyMethodDef module_methods[] = {
	//{"test", (PyCFunction)pyfastx_test, METH_NOARGS, NULL},
	//{"clean_seq", clean_seq, METH_VARARGS, NULL},
	//{"sub_seq", sub_seq, METH_VARARGS, NULL},
	{"version", (PyCFunction)pyfastx_version, METH_VARARGS | METH_KEYWORDS, NULL},
	{"gzip_check", (PyCFunction)pyfastx_gzip_check, METH_VARARGS, NULL},
	{NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
	static struct PyModuleDef module_pyfastx = {
		PyModuleDef_HEAD_INIT,
		"pyfastx",
		"A python C extension for parsing fasta and fastq file",
		-1,
		module_methods,
	};
#endif

static PyObject* pyfastx_module_init(void){
	PyObject *module;

#if PY_MAJOR_VERSION >= 3
	module = PyModule_Create(&module_pyfastx);

#else
	module = Py_InitModule("pyfastx", module_methods);
#endif

	if (module == NULL){
		return NULL;
	}

	if(PyType_Ready(&pyfastx_FastaType) < 0){
		return NULL;
	}
	Py_INCREF((PyObject *)&pyfastx_FastaType);
	PyModule_AddObject(module, "Fasta", (PyObject *)&pyfastx_FastaType);

	if(PyType_Ready(&pyfastx_FastqType) < 0){
		return NULL;
	}
	Py_INCREF((PyObject *)&pyfastx_FastqType);
	PyModule_AddObject(module, "Fastq", (PyObject *)&pyfastx_FastqType);

	if(PyType_Ready(&pyfastx_FastxType) < 0){
		return NULL;
	}
	Py_INCREF((PyObject *)&pyfastx_FastxType);
	PyModule_AddObject(module, "Fastx", (PyObject *)&pyfastx_FastxType);

	if(PyType_Ready(&pyfastx_SequenceType) < 0){
		return NULL;
	}
	Py_INCREF((PyObject *)&pyfastx_SequenceType);
	PyModule_AddObject(module, "Sequence", (PyObject *)&pyfastx_SequenceType);

	
	if(PyType_Ready(&pyfastx_ReadType) < 0){
		return NULL;
	}
	Py_INCREF((PyObject *)&pyfastx_ReadType);
	PyModule_AddObject(module, "Read", (PyObject *)&pyfastx_ReadType);

	if(PyType_Ready(&pyfastx_FastaKeysType) < 0){
		return NULL;
	}
	Py_INCREF((PyObject *)&pyfastx_FastaKeysType);
	PyModule_AddObject(module, "FastaKeys", (PyObject *)&pyfastx_FastaKeysType);

	if (PyType_Ready(&pyfastx_FastqKeysType) < 0) {
		return NULL;
	}
	Py_INCREF((PyObject *)&pyfastx_FastqKeysType);
	PyModule_AddObject(module, "FastqKeys", (PyObject *)&pyfastx_FastqKeysType);

	return module;
}

#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC PyInit_pyfastx() {
	return pyfastx_module_init();
}
#else
PyMODINIT_FUNC initpyfastx(void) {
	pyfastx_module_init();
}
#endif