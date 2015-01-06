<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="text" indent="no"/>
<!-- IP address ranges tranform to comma dilimited output -->
<!-- This transform parses and outputs the list of IP Address ranges. From Asset Groups-->
<!-- The following element is used for carriage return characters <xsl:text>&#10;
</xsl:text> -->


<!-- example: xsltproc IP_trans.xsl qualys_assetgroup_list.xml -->

<xsl:strip-space elements="*"/>
<xsl:template match="/">
<!-- <xsl:value-of select="TITLE"/>,<xsl:value-of select="SCANIPS/IP"/> <xsl:text>&#10;</xsl:text> -->
<xsl:for-each select="ASSET_GROUP_LIST/ASSET_GROUP">
<!-- Asset Group Title:	<xsl:value-of select="TITLE"/><xsl:text>&#10;</xsl:text> -->
	<xsl:variable name="AssetTitle" select="TITLE"/>
	<xsl:for-each select="SCANIPS">
		<xsl:for-each select="node()">
			<xsl:value-of select="$AssetTitle"/>, <xsl:value-of select="."/><xsl:text>&#10;</xsl:text>
    	</xsl:for-each>
	</xsl:for-each>
</xsl:for-each>
<!-- <xsl:value-of select="SCANIPS/IP"/> <xsl:text>&#10;</xsl:text> -->
</xsl:template>
</xsl:stylesheet>