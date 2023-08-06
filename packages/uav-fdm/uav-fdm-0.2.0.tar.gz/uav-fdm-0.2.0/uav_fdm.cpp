#include "uav_fdm.h"

#include "uav_fdm3d.h"

#define CAPI_MDL uav_fdm3d

#define CAT_I(a, b) a##b
#define CAT(a, b) CAT_I(a, b)

#define ap_GetCAPIStaticMap_fcn CAT(CAPI_MDL,_GetCAPIStaticMap)

#define M_PI (3.14159265354)

#include <iostream>
#include <fstream>
#include <vector>
#include <regex>
#include <string>

std::vector<std::string> scan_param(uav_fdmModelClass *Obj)
{
    std::vector<std::string> head;

    const rtwCAPI_ModelMappingStaticInfo *sm = ap_GetCAPIStaticMap_fcn();
	
    if (sm)
    {
        //unsigned int n = rtwCAPI_GetNumBlockParametersFromStaticMap(sm);
        unsigned int m = rtwCAPI_GetNumModelParametersFromStaticMap(sm);
        rtwCAPI_ModelParameters const *prm = rtwCAPI_GetModelParametersFromStaticMap(sm);
        rtwCAPI_DataTypeMap const *dtm = rtwCAPI_GetDataTypeMapFromStaticMap(sm);
        rtwCAPI_DimensionMap const *dmm = rtwCAPI_GetDimensionMapFromStaticMap(sm);
        uint_T const *dam = rtwCAPI_GetDimensionArrayFromStaticMap(sm);
        rtwCAPI_ModelMappingInfo *MMI = &(rtmGetDataMapInfo(Obj->getRTM()).mmi);
        void **da = rtwCAPI_GetDataAddressMap(MMI);
        for (unsigned int i = 0; i < m; ++i)
        {
            const char *name = rtwCAPI_GetModelParameterName(prm, i);
            int idx = rtwCAPI_GetModelParameterAddrIdx(prm, i);
            uint16_t dti = rtwCAPI_GetModelParameterDataTypeIdx(prm, i);
            uint16_t dmi = rtwCAPI_GetModelParameterDimensionIdx(prm, i);
            uint8_t ss = rtwCAPI_GetDataTypeSLId(dtm, dti);
            uint16_t dai = rtwCAPI_GetDimArrayIndex(dmm, dmi);
            uint8_t nd = rtwCAPI_GetNumDims(dmm, dmi);
            uint16_t n = 1;
            for (int j = 0; j < nd; ++j)
            {
                n *= dam[dai + j];
            }
            head.push_back(std::string(name));
            for (int j = 1; j < n; ++j)
            {
                head.push_back(std::string(name) + "(" + std::to_string(j) + ")");
            }
        }
    }
    return head;
}

void setup_param(uav_fdmModelClass *Obj, const std::vector<std::string> &head, const std::vector<double> &onecase)
{
    const rtwCAPI_ModelMappingStaticInfo *sm = ap_GetCAPIStaticMap_fcn();
    if (sm)
    {
        //unsigned int n = rtwCAPI_GetNumBlockParametersFromStaticMap(sm);
        unsigned int m = rtwCAPI_GetNumModelParametersFromStaticMap(sm);
        rtwCAPI_ModelParameters const *prm = rtwCAPI_GetModelParametersFromStaticMap(sm);
        rtwCAPI_DataTypeMap const *dtm = rtwCAPI_GetDataTypeMapFromStaticMap(sm);
        rtwCAPI_DimensionMap const *dmm = rtwCAPI_GetDimensionMapFromStaticMap(sm);
        uint_T const *dam = rtwCAPI_GetDimensionArrayFromStaticMap(sm);
        rtwCAPI_ModelMappingInfo *MMI = &(rtmGetDataMapInfo(Obj->getRTM()).mmi);
        void **da = rtwCAPI_GetDataAddressMap(MMI);
        for (unsigned int i = 0; i < m; ++i)
        {
            const char *name = rtwCAPI_GetModelParameterName(prm, i);
            int idx = rtwCAPI_GetModelParameterAddrIdx(prm, i);
            uint16_t dti = rtwCAPI_GetModelParameterDataTypeIdx(prm, i);
            uint16_t dmi = rtwCAPI_GetModelParameterDimensionIdx(prm, i);
            uint8_t ss = rtwCAPI_GetDataTypeSLId(dtm, dti);
            uint16_t dai = rtwCAPI_GetDimArrayIndex(dmm, dmi);
            uint8_t nd = rtwCAPI_GetNumDims(dmm, dmi);
            uint16_t n = 1;
            for (int j = 0; j < nd; ++j)
            {
                n *= dam[dai + j];
            }
            int j = 0;
            for (auto i = head.begin(); i != head.end(); ++i, ++j)
            {
                if (i->find(name) != std::string::npos)
                {
                    int param_idx = 0;
                    double param_value = onecase[j];
                    std::smatch result;
					std::regex pattern("(.*)\\((\\d{1,})\\)");
                    if (std::regex_match(*i, result, pattern))
                    {
                        param_idx = std::stoi(result[2].str());
                    }
                    switch (ss)
                    {
                    case SS_DOUBLE:
                    {
                        double *d = (double *)da[idx];
                        d[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << d[param_idx] << std::endl;
                    }
                    break;
                    case SS_SINGLE:
                    {
                        float *s = (float *)da[idx];
                        s[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << s[param_idx] << std::endl;
                    }
                    break;
                    case SS_INT8:
                    {
                        int8_T *c = (int8_T *)da[idx];
                        c[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << (int)c[param_idx] << std::endl;

                    }
                    break;
                    case SS_INT16:
                    {
                        int16_T *h = (int16_T *)da[idx];
                        h[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << h[param_idx] << std::endl;
                    }
                    break;
                    case SS_INT32:
                    {
                        int32_T *I = (int32_T *)da[idx];
                        I[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << I[param_idx] << std::endl;
                    }
                    break;
                    case SS_UINT8:
                    {
                        uint8_T *c = (uint8_T *)da[idx];
                        c[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << (int)c[param_idx] << std::endl;
                    }
                    break;
                    case SS_UINT16:
                    {
                        uint16_T *h = (uint16_T *)da[idx];
                        h[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << h[param_idx] << std::endl;
                    }
                    break;
                    case SS_UINT32:
                    {
                        uint32_T *I = (uint32_T *)da[idx];
                        I[param_idx] = param_value;
						std::cout << name << "(" <<  param_idx  << ")=" << I[param_idx] << std::endl;
                    }
                    break;
                    }
                }
            }
        }
    }
}

const double lat2m = 110574.2727;
const double lon2m = 111319.46;

uav_fdm::uav_fdm(double x0, double y0, double alt0,
            double gs0, double gamma0, double psi0, double phi0)
{
    fdm3d = new uav_fdmModelClass;

        std::cout << "Parameters in the mdl:" << std::endl;
        std::vector<std::string> heads = scan_param(fdm3d);
        for (auto i = heads.begin(); i != heads.end(); ++i)
        {
            std::cout << '\t' << *i << std::endl;
        }
        std::vector<std::string> param_name;
        std::vector<double> param_val;
        param_name.push_back("LatLon0");
        param_val.push_back(x0/lat2m);
        param_name.push_back("LatLon0(1)");
        param_val.push_back(y0/lat2m);
        param_name.push_back("Alt0");
        param_val.push_back(alt0);
        param_name.push_back("gs0");
        param_val.push_back(gs0);
        param_name.push_back("gamma0");
        param_val.push_back(gamma0);
        param_name.push_back("psi0");
        param_val.push_back(psi0);
        param_name.push_back("phi0");
        param_val.push_back(phi0);
        setup_param(fdm3d, param_name, param_val);

    fdm3d->initialize();
}

void uav_fdm::update(double dt, double tas_c, double hdot_c, double psi_c,
                double w_n, double w_e,
                double *time_stamp,
                double *x, double *y, double *alt,
                double *v_n, double *v_e, double *hdot,
                double *phi, 
                double *psi_t, double *gamma, double *gs,
                double *tas)
{
    double t0 = fdm3d->uav_fdm3d_Y.time_stamp;
    fdm3d->uav_fdm3d_U.tas_c = tas_c;
    fdm3d->uav_fdm3d_U.hdot_c = hdot_c;
    fdm3d->uav_fdm3d_U.w_n = w_n;
    fdm3d->uav_fdm3d_U.w_e = w_e;
    double phi_c;
    double dpsi = psi_c - fdm3d->uav_fdm3d_Y.psi_t;
    while (dpsi > M_PI)
    {
        dpsi -= 2 * M_PI;
    }
    while (dpsi < -M_PI)
    {
        dpsi += 2 * M_PI;
    }
    double as_c = dpsi * fdm3d->uav_fdm3d_Y.gs;
    if (as_c > 5)
        as_c = 5;
    else if (as_c < -5)
        as_c = -5;
    fdm3d->uav_fdm3d_U.phi_c = atan2(as_c, 9.8);

    do {
      fdm3d->step();
      *time_stamp = fdm3d->uav_fdm3d_Y.time_stamp;
    } while (*time_stamp - t0 < dt);
    *x = fdm3d->uav_fdm3d_Y.lat * lat2m;
    *y = fdm3d->uav_fdm3d_Y.lon * lon2m;
    *alt = fdm3d->uav_fdm3d_Y.ASL;
    *v_n = fdm3d->uav_fdm3d_Y.Vn;
    *v_e = fdm3d->uav_fdm3d_Y.Ve;
    *hdot = fdm3d->uav_fdm3d_Y.hdot;
    *phi = fdm3d->uav_fdm3d_Y.phi;
    *psi_t = fdm3d->uav_fdm3d_Y.psi_t;
    *gamma = fdm3d->uav_fdm3d_Y.gamma;
    *gs = fdm3d->uav_fdm3d_Y.gs;
    *tas = fdm3d->uav_fdm3d_Y.tas;
}
