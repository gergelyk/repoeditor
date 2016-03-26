<?xml version="1.0" encoding="ISO-8859-1" ?> 
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
    <html>
    <head>
        <title>Summary</title> 
        <style>
        body {
            background-color: linen;
            margin-left: 5%;
            font-family: sans-serif;
        }

        h2 {
            color: darkblue;
        }
        
        table, th, td {
           border: 1px solid darkblue;
        }
        
        table {
            border-collapse: collapse;
            width: 90%;
        }

        td, th {
            padding: 5px;
        }

        th {
            height: 30px;
            text-align: left;
            background-color: darkblue;
            color: linen;
        }

        tr.package td {
            font-weight: bold;
            background-color: peachpuff ;
        }
        
        tr.version td {
            font-family: monospace;
        }
        
        a {
            font-family: monospace;
            font-weight: normal;
        }
        </style>
    </head>
    <body>
        <h2>Available Packages</h2> 
        <table>
        <tr>
        <th>Category</th> 
        <th>Title / Version</th> 
        <th>Description / URL</th> 
        </tr>

        <xsl:for-each select="root/package">
        <xsl:variable name="vPackage" select="@name"/>
        <tr class="package">
        <td><xsl:value-of select="category"/></td>
        <td><xsl:value-of select="title"/></td>
        <td>
        <xsl:value-of select="description"/><br/><a><xsl:value-of select="url"/></a>
        </td>
        </tr>
            <xsl:for-each select="../version[@package = $vPackage]">
            <tr  class="version">
            <td></td>
            <td><xsl:value-of select="@name"/> </td>
            <td><xsl:value-of select="url"/> </td>
            </tr>
            </xsl:for-each>
        </xsl:for-each>

        </table>
    </body>
    </html>
</xsl:template>
</xsl:stylesheet>
