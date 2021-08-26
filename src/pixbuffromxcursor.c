/*
 *  Copyright (c) 2008-2011 Nick Schermer <nick@xfce.org>
 *  Copyright (c) 2008      Jannis Pohlmann <jannis@xfce.org>
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Library General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License along
 *  with this program; if not, write to the Free Software Foundation, Inc.,
 *  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#include <Python.h>
#include <pygobject.h>

#include <X11/Xcursor/Xcursor.h>
#include <gdk-pixbuf/gdk-pixbuf.h>

#define PREVIEW_SIZE (24)

static GdkPixbuf *
mouse_settings_themes_pixbuf_from_filename (const gchar *filename,
                                            guint        size)
{
    XcursorImage *image;
    GdkPixbuf    *scaled, *pixbuf = NULL;
    gsize         bsize;
    guchar       *buffer, *p, tmp;
    gdouble       wratio, hratio;
    gint          dest_width, dest_height;

    /* load the image */
    image = XcursorFilenameLoadImage (filename, size);
    if (G_LIKELY (image))
    {
        /* buffer size */
        bsize = image->width * image->height * 4;

        /* allocate buffer */
        buffer = g_malloc (bsize);

        /* copy pixel data to buffer */
        memcpy (buffer, image->pixels, bsize);

        /* swap bits */
        for (p = buffer; p < buffer + bsize; p += 4)
        {
            tmp = p[0];
            p[0] = p[2];
            p[2] = tmp;
        }

        /* create pixbuf */
        pixbuf = gdk_pixbuf_new_from_data (buffer, GDK_COLORSPACE_RGB, TRUE,
                                           8, image->width, image->height,
                                           4 * image->width,
                                           (GdkPixbufDestroyNotify) (void (*)(void)) g_free, NULL);

        /* don't leak when creating the pixbuf failed */
        if (G_UNLIKELY (pixbuf == NULL))
            g_free (buffer);

        /* scale pixbuf if needed */
        if (pixbuf && (image->height > size || image->width > size))
        {
            /* calculate the ratio */
            wratio = (gdouble) image->width / (gdouble) size;
            hratio = (gdouble) image->height / (gdouble) size;

            /* init */
            dest_width = dest_height = size;

            /* set dest size */
            if (hratio > wratio)
                dest_width  = rint (image->width / hratio);
            else
                dest_height = rint (image->height / wratio);

            /* scale pixbuf */
            scaled = gdk_pixbuf_scale_simple (pixbuf, MAX (dest_width, 1), MAX (dest_height, 1), GDK_INTERP_BILINEAR);

            /* release and set scaled pixbuf */
            g_object_unref (G_OBJECT (pixbuf));
            pixbuf = scaled;
        }

        /* cleanup */
        XcursorImageDestroy (image);
    }

    return pixbuf;
}

static PyObject *
pixbufFromXCursor (PyObject *self,
                   PyObject *args)
{
    char      *path = NULL;
    GdkPixbuf *pixbuf = NULL;
    PyObject  *object;

    if (!PyArg_ParseTuple (args, "s", &path))
        return NULL;

    pixbuf = mouse_settings_themes_pixbuf_from_filename (path, PREVIEW_SIZE);
    object = pygobject_new (G_OBJECT (pixbuf));
    return object;
}

static PyMethodDef methods[] = {
    {"pixbufFromXCursor", pixbufFromXCursor, METH_VARARGS, "Generates a GdkPixbuf from a given file path"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "pixbuffromxcursor",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC
PyInit_pixbuffromxcursor (void)
{
    pygobject_init (3, 0 ,0);

    return PyModule_Create (&module);
}