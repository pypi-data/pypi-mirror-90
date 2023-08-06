#include "fakeys.h"
#include "util.h"

char SORTS[][6] = {"ID", "chrom", "slen"};
char ORDERS[][5] = {"ASC", "DESC"};

void pyfastx_fasta_keys_dealloc(pyfastx_FastaKeys *self){
	if (self->stmt) {
		PYFASTX_SQLITE_CALL(sqlite3_finalize(self->stmt));
	}

	if (self->temp_filter) {
		free(self->temp_filter);
	}

	if (self->filter) {
		free(self->filter);
	}

	Py_TYPE(self)->tp_free((PyObject *)self);
}

void create_temp_query_set(pyfastx_FastaKeys *self) {
	char *sql;
	PYFASTX_SQLITE_CALL(sqlite3_exec(self->index_db, "DROP TABLE tmp", NULL, NULL, NULL));
	if (self->filter) {
		sql = sqlite3_mprintf("CREATE TEMP TABLE tmp AS SELECT chrom FROM seq WHERE %s ORDER BY %s %s",
			self->filter, SORTS[self->sort], ORDERS[self->order]);
	} else {
		sql = sqlite3_mprintf("CREATE TEMP TABLE tmp AS SELECT chrom FROM seq ORDER BY %s %s",
			SORTS[self->sort], ORDERS[self->order]);
	}
	PYFASTX_SQLITE_CALL(sqlite3_exec(self->index_db, sql, NULL, NULL, NULL));
	sqlite3_free(sql);
	self->update = 0;
}

PyObject *pyfastx_fasta_keys_iter(pyfastx_FastaKeys *self) {
	char *sql;

	if (self->filter || self->sort || self->order) {
		if (self->update) {
			create_temp_query_set(self);
		}
		sql = sqlite3_mprintf("SELECT chrom FROM tmp ORDER BY rowid");
	} else {
		sql = sqlite3_mprintf("SELECT chrom FROM seq ORDER BY ID");
	}

	if (self->stmt) {
		PYFASTX_SQLITE_CALL(sqlite3_finalize(self->stmt));
		self->stmt = NULL;
	}

	PYFASTX_SQLITE_CALL(sqlite3_prepare_v2(self->index_db, sql, -1, &self->stmt, NULL));
	sqlite3_free(sql);

	Py_INCREF(self);
	return (PyObject *)self;
}

PyObject *pyfastx_fasta_keys_next(pyfastx_FastaKeys *self){
	int nbytes;
	char *name;
	int ret;

	if (!self->stmt) {
		PyErr_SetString(PyExc_TypeError, "'FaKeys' object is not an iterator");
		return NULL;
	}

	PYFASTX_SQLITE_CALL(ret=sqlite3_step(self->stmt));

	if (ret == SQLITE_ROW){
		PYFASTX_SQLITE_CALL(
			nbytes = sqlite3_column_bytes(self->stmt, 0);
			name = (char *)malloc(nbytes + 1);
			memcpy(name, (char *)sqlite3_column_text(self->stmt, 0), nbytes);
		);
		name[nbytes] = '\0';
		return Py_BuildValue("s", name);
	}

	PYFASTX_SQLITE_CALL(sqlite3_finalize(self->stmt));
	self->stmt = NULL;
	return NULL;
}

uint64_t pyfastx_fasta_keys_length(pyfastx_FastaKeys *self){
	return self->seq_counts;
}

PyObject *pyfastx_fasta_keys_repr(pyfastx_FastaKeys *self){
	return PyUnicode_FromFormat("<FastaKeys> contains %ld keys", self->seq_counts);
}

PyObject *pyfastx_fasta_keys_item(pyfastx_FastaKeys *self, Py_ssize_t i){
	sqlite3_stmt *stmt;
	char *sql;
	int ret;
	int nbytes;
	char *name;
	
	if (i < 0){
		i = i + self->seq_counts;
	}

	++i;

	if (i > self->seq_counts){
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	if (self->filter || self->sort || self->order) {
		if (self->update) {
			create_temp_query_set(self);
		}
		sql = sqlite3_mprintf("SELECT chrom FROM tmp WHERE rowid=?");
	} else {
		sql = sqlite3_mprintf("SELECT chrom FROM seq WHERE ID=?");
	}
	
	PYFASTX_SQLITE_CALL(sqlite3_prepare_v2(self->index_db, sql, -1, &stmt, NULL));
	sqlite3_free(sql);

	PYFASTX_SQLITE_CALL(
		sqlite3_bind_int(stmt, 1, i);
		ret = sqlite3_step(stmt);
	);

	if (ret == SQLITE_ROW) {
		PYFASTX_SQLITE_CALL(nbytes = sqlite3_column_bytes(stmt, 0));
		name = (char *)malloc(nbytes + 1);
		PYFASTX_SQLITE_CALL(memcpy(name, (char *)sqlite3_column_text(stmt, 0), nbytes));
		name[nbytes] = '\0';
		PYFASTX_SQLITE_CALL(sqlite3_finalize(stmt));
		return Py_BuildValue("s", name);
	} else {
		PYFASTX_SQLITE_CALL(sqlite3_finalize(stmt));
		PyErr_Format(PyExc_ValueError, "get item error, code: %d", ret);
		return NULL;
	}
}

int pyfastx_fasta_keys_contains(pyfastx_FastaKeys *self, PyObject *key){
	char *name;
	sqlite3_stmt *stmt;
	char *sql;
	int ret;

	if (!PyUnicode_CheckExact(key)) {
		return 0;
	}

	name = (char *)PyUnicode_AsUTF8(key);

	if (self->filter || self->sort || self->order) {
		if (self->update) {
			create_temp_query_set(self);
		}
		sql = sqlite3_mprintf("SELECT 1 FROM tmp WHERE chrom=? LIMIT 1");
	} else {
		sql = sqlite3_mprintf("SELECT 1 FROM seq WHERE chrom=? LIMIT 1");
	}

	PYFASTX_SQLITE_CALL(
		sqlite3_prepare_v2(self->index_db, sql, -1, &stmt, NULL);
		sqlite3_free(sql);
		sqlite3_bind_text(stmt, 1, name, -1, NULL);
		ret = sqlite3_step(stmt);
		sqlite3_finalize(stmt);
	);

	return ret==SQLITE_ROW ? 1 : 0;
}

PyObject *pyfastx_fasta_keys_sort(pyfastx_FastaKeys *self, PyObject *args, PyObject *kwargs) {
	char *key = "id";
	int reverse = 0;
	
	static char* kwlist[] = {"by", "reverse", NULL};

	// cannot use uint16_t to parse Python bool, should use int declare
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|si", kwlist, &key, &reverse)) {
		return NULL;
	}

	//set sort column
	if (strcmp(key, "id") == 0) {
		self->sort = 0;
	} else if (strcmp(key, "name") == 0) {
		self->sort = 1;
	} else if (strcmp(key, "length") == 0) {
		self->sort = 2;
	} else {
		PyErr_SetString(PyExc_ValueError, "key only can be id, name or length");
		return NULL;
	}

	//set sort order
	self->order = reverse;

	//need to update
	self->update = 1;

	Py_INCREF(self);
	return (PyObject *)self;
}

PyObject *pyfastx_fasta_keys_richcompare(pyfastx_FastaKeys *self, PyObject *other, int op) {
	char *when;
	uint32_t slen;
	char signs[][3] = {"<", "<=", "=", "<>", ">", ">="};
	int signt = 0;

	if (!PyLong_Check(other)) {
		PyErr_SetString(PyExc_ValueError, "the compared item must be an integer");
		return NULL;
	}

	slen = PyLong_AsLong(other);
	
	switch (op) {
		case Py_LT: signt = 0; break;
		case Py_LE: signt = 1; break;
		case Py_EQ: signt = 2; break;
		case Py_NE: signt = 3; break;
		case Py_GT: signt = 4; break;
		case Py_GE: signt = 5; break;
	}

	if (self->temp_filter) {
		when = sqlite3_mprintf(" AND slen %s %d", signs[signt], slen);
		self->temp_filter = (char *)realloc(self->temp_filter, strlen(self->temp_filter) + strlen(when) + 1);
		strcat(self->temp_filter, when);
		sqlite3_free(when);
	} else {
		when = sqlite3_mprintf("slen %s %d", signs[signt], slen);
		self->temp_filter = (char *)malloc(strlen(when) + 1);
		strcpy(self->temp_filter, when);
		sqlite3_free(when);
	}

	return Py_BuildValue("s", self->temp_filter);
}

PyObject *pyfastx_fasta_keys_like(pyfastx_FastaKeys *self, PyObject *tag) {
	if (!PyUnicode_CheckExact(tag)) {
		PyErr_SetString(PyExc_ValueError, "the tag after % must be a string");
		return NULL;
	}

	return PyUnicode_FromFormat("chrom LIKE '%%%s%%'", (char *)PyUnicode_AsUTF8(tag));
}

PyObject *pyfastx_fasta_keys_filter(pyfastx_FastaKeys *self, PyObject *args) {
	sqlite3_stmt *stmt;
	char *sql;
	char *tmp;
	int ret;
	Py_ssize_t l;
	Py_ssize_t c = PyTuple_Size(args);

	if (!c) {
		PyErr_SetString(PyExc_ValueError, "no comparison condition provided");
		return NULL;
	}

	PyObject *sep = Py_BuildValue("s", " AND ");
	PyObject *cat = PyUnicode_Join(sep, args);
	tmp = (char *)PyUnicode_AsUTF8AndSize(cat, &l);

	if (self->filter) {
		self->filter = (char *)realloc(self->filter, l+1);
	} else {
		self->filter = (char *)malloc(l+1);
	}
	
	strcpy(self->filter, tmp);
	Py_DECREF(sep);
	Py_DECREF(cat);
	
	if (self->temp_filter) {
		free(self->temp_filter);
		self->temp_filter = NULL;
	}

	sql = sqlite3_mprintf("SELECT COUNT(*) FROM seq WHERE %s", self->filter);

	PYFASTX_SQLITE_CALL(sqlite3_prepare_v2(self->index_db, sql, -1, &stmt, NULL));
	sqlite3_free(sql);

	PYFASTX_SQLITE_CALL(ret=sqlite3_step(stmt));

	if (ret == SQLITE_ROW) {
		PYFASTX_SQLITE_CALL(self->seq_counts = sqlite3_column_int64(stmt, 0));
	} else {
		self->seq_counts = 0;
	}

	PYFASTX_SQLITE_CALL(sqlite3_finalize(stmt));

	//need to update
	self->update = 1;

	Py_INCREF(self);
	return (PyObject *)self;
}

PyObject *pyfastx_fasta_keys_reset(pyfastx_FastaKeys *self) {
	sqlite3_stmt *stmt;
	int ret;
	
	self->sort = 0;
	self->order = 0;

	if (self->filter) {
		free(self->filter);
		self->filter = NULL;
	}

	if (self->temp_filter) {
		free(self->temp_filter);
		self->temp_filter = NULL;
	}

	PYFASTX_SQLITE_CALL(sqlite3_exec(self->index_db, "DROP TABLE tmp", NULL, NULL, NULL));
	self->update = 0;
	
	PYFASTX_SQLITE_CALL(
		sqlite3_prepare_v2(self->index_db, "SELECT seqnum FROM stat", -1, &stmt, NULL);
		ret = sqlite3_step(stmt);
	);

	if (ret == SQLITE_ROW) {
		PYFASTX_SQLITE_CALL(
			self->seq_counts = sqlite3_column_int64(stmt, 0);
			sqlite3_finalize(stmt);
		);
	} else {
		PYFASTX_SQLITE_CALL(sqlite3_finalize(stmt));
		PyErr_SetString(PyExc_RuntimeError, "get sequence counts error");
		return NULL;
	}

	Py_INCREF(self);
	return (PyObject *)self;
}

static PyMethodDef pyfastx_fasta_keys_methods[] = {
	{"sort", (PyCFunction)pyfastx_fasta_keys_sort, METH_VARARGS|METH_KEYWORDS, NULL},
	{"filter", (PyCFunction)pyfastx_fasta_keys_filter, METH_VARARGS, NULL},
	{"reset", (PyCFunction)pyfastx_fasta_keys_reset, METH_NOARGS, NULL},
	{NULL, NULL, 0, NULL}
};

//as a number
static PyNumberMethods fasta_keys_as_number = {
	0,
	0,
	0,
	(binaryfunc)pyfastx_fasta_keys_like,
	0,
};

//as a list
static PySequenceMethods fasta_keys_as_sequence = {
	(lenfunc)pyfastx_fasta_keys_length, /*sq_length*/
	0, /*sq_concat*/
	0, /*sq_repeat*/
	(ssizeargfunc)pyfastx_fasta_keys_item, /*sq_item*/
	0, /*sq_slice */
	0, /*sq_ass_item*/
	0, /*sq_ass_splice*/
	(objobjproc)pyfastx_fasta_keys_contains, /*sq_contains*/
	0, /*sq_inplace_concat*/
	0, /*sq_inplace_repeat*/
};

PyTypeObject pyfastx_FastaKeysType = {
    //PyVarObject_HEAD_INIT(&PyType_Type, 0)
    PyVarObject_HEAD_INIT(NULL, 0)
    "Identifier",                     /* tp_name */
    sizeof(pyfastx_FastaKeys),       /* tp_basicsize */
    0,                              /* tp_itemsize */
    (destructor)pyfastx_fasta_keys_dealloc,                              /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_reserved */
    (reprfunc)pyfastx_fasta_keys_repr,                              /* tp_repr */
    &fasta_keys_as_number,                              /* tp_as_number */
    &fasta_keys_as_sequence,                              /* tp_as_sequence */
    0,   /* tp_as_mapping */
    0,                              /* tp_hash */
    0,                              /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,             /* tp_flags */
    0,                              /* tp_doc */
    0,                              /* tp_traverse */
    0,                              /* tp_clear */
    (richcmpfunc)pyfastx_fasta_keys_richcompare,                              /* tp_richcompare */
    0,                              /* tp_weaklistoffset */
    (getiterfunc)pyfastx_fasta_keys_iter,                              /* tp_iter */
    (iternextfunc)pyfastx_fasta_keys_next,                              /* tp_iternext */
    pyfastx_fasta_keys_methods,       /* tp_methods */
    0,       /* tp_members */
    0,       /* tp_getset */
    0,                              /* tp_base */
    0,                              /* tp_dict */
    0,                              /* tp_descr_get */
    0,                              /* tp_descr_set */
    0,                              /* tp_dictoffset */
    0,                              /* tp_init */
    PyType_GenericAlloc,            /* tp_alloc */
    PyType_GenericNew,           /* tp_new */
};