#include <iostream>

#include <gdal.h>
#include <gdal_priv.h>
#include <ogr_geometry.h>
#include <ogrsf_frmts.h>
#include <geos_c.h>
#include <geodesic.h>

size_t coordDistanceInM(double x1, double y1, double x2, double y2) {
  struct geod_geodesic g;
  geod_init(&g, 6378137, 1/298.257223563); // we're on Earth

  // Let's be reeeeeally clear here :)
  // latitude = north/south. That's "y" in these numbers. You can tell because
  // we're talking about Texas and the "y" is positive and "x" is negative.
  double lat1 = y1;
  double lat2 = y2;
  double lon1 = x1;
  double lon2 = x2;

  double ret, _1, _2;
  geod_inverse(&g, lat1, lon1, lat2, lon2, &ret, &_1, &_2);

  return ret;
}

size_t geometryDistanceInM(const OGRGeometry& g1, const OGRGeometry& g2) {
  GEOSContextHandle_t context = OGRGeometry::createGEOSContext();
  GEOSGeom geom1 = g1.exportToGEOS(context);
  GEOSGeom geom2 = g2.exportToGEOS(context);

  GEOSCoordSequence* coords = GEOSNearestPoints_r(context, geom1, geom2);
  double x1, y1, x2, y2;
  GEOSCoordSeq_getX_r(context, coords, 0, &x1);
  GEOSCoordSeq_getY_r(context, coords, 0, &y1);
  GEOSCoordSeq_getX_r(context, coords, 1, &x2);
  GEOSCoordSeq_getY_r(context, coords, 1, &y2);

  GEOSCoordSeq_destroy_r(context, coords);
  GEOSGeom_destroy_r(context, geom1);
  GEOSGeom_destroy_r(context, geom2);
  OGRGeometry::freeGEOSContext(context);

  return coordDistanceInM(x1, y1, x2, y2);
}

int main(int argc, char** argv) {
  GDALAllRegister();

  GDALDataset* mexicoDs = reinterpret_cast<GDALDataset*>(GDALOpenEx("../data/mexico-buffered.shp", GDAL_OF_VECTOR, NULL, NULL, NULL));
  if (!mexicoDs) {
    std::cerr << "Could not open Mexico" << std::endl;
    return 1;
  }

  GDALDataset* vtdDs = reinterpret_cast<GDALDataset*>(GDALOpenEx("../data/vtd16g.shp", GDAL_OF_VECTOR, NULL, NULL, NULL));
  if (!vtdDs) {
    std::cerr << "Could not open Texas" << std::endl;
    return 1;
  }

  auto* mexicoLayer = mexicoDs->GetLayer(0);
  auto* vtdLayer = vtdDs->GetLayer(0);

  auto* mexicoCrs = mexicoLayer->GetSpatialRef();
  auto* vtdCrs = vtdLayer->GetSpatialRef();

  // Mexico is already WGS84. We'll project Texas features back to that, so we
  // can calculate spherical distances.
  const auto toWgs84 = OGRCreateCoordinateTransformation(vtdCrs, mexicoCrs);

  auto* mexicoFeature = mexicoLayer->GetNextFeature();
  auto* mexicoGeo = mexicoFeature->GetGeometryRef();

  std::cout << "CNTYVTD,metersFromMexico" << std::endl;

  OGRFeature* vtdFeature;
  while ((vtdFeature = vtdLayer->GetNextFeature()) != NULL) {
    const char* cntyvtd = vtdFeature->GetFieldAsString("CNTYVTD");
    auto* vtdGeo = vtdFeature->GetGeometryRef();
    OGRErr err = vtdGeo->transform(toWgs84);
    if (err != 0) {
      std::cerr << "Transform of feature " << cntyvtd << " failed" << std::endl;
      return 1;
    }
    size_t distance = geometryDistanceInM(*mexicoGeo, *vtdGeo);

    std::cout << cntyvtd << "," << distance << std::endl;
    OGRFeature::DestroyFeature(vtdFeature);
  }

  GDALClose(vtdDs);
  GDALClose(mexicoDs);

  return 0;
}
