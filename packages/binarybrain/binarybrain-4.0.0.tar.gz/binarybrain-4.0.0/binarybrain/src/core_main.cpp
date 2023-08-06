// --------------------------------------------------------------------------
//  Binary Brain  -- binary neural net framework
//
//                                Copyright (C) 2018-2020 by Ryuji Fuchikami
//                                https://github.com/ryuz
//                                ryuji.fuchikami@nifty.com
// --------------------------------------------------------------------------


#define BB_PYBIND11


#include <omp.h>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include <pybind11/numpy.h>


#include "bb/Version.h"
#include "bb/DataType.h"

#include "bb/Tensor.h"
#include "bb/FrameBuffer.h"
#include "bb/Variables.h"

#include "bb/RealToBinary.h"
#include "bb/BinaryToReal.h"
#include "bb/BinaryModulation.h"
#include "bb/BitEncode.h"
#include "bb/Reduce.h"

#include "bb/Sequential.h"
#include "bb/DenseAffine.h"
#include "bb/DepthwiseDenseAffine.h"
#include "bb/DifferentiableLutN.h"
#include "bb/DifferentiableLutDiscreteN.h"
#include "bb/MicroMlp.h"
#include "bb/BinaryLutN.h"

#include "bb/Convolution2d.h"
#include "bb/MaxPooling.h"
#include "bb/StochasticMaxPooling.h"
#include "bb/StochasticMaxPooling2x2.h"
#include "bb/UpSampling.h"

#include "bb/Binarize.h"
#include "bb/Sigmoid.h"
#include "bb/ReLU.h"
#include "bb/HardTanh.h"

#include "bb/BatchNormalization.h"
#include "bb/StochasticBatchNormalization.h"
#include "bb/Dropout.h"
#include "bb/Shuffle.h"

#include "bb/LossFunction.h"
#include "bb/LossSoftmaxCrossEntropy.h"
#include "bb/LossMeanSquaredError.h"

#include "bb/MetricsFunction.h"
#include "bb/MetricsCategoricalAccuracy.h"
#include "bb/MetricsMeanSquaredError.h"

#include "bb/Optimizer.h"
#include "bb/OptimizerSgd.h"
#include "bb/OptimizerAdam.h"
#include "bb/OptimizerAdaGrad.h"

#include "bb/ExportVerilog.h"


#include "bb/ValueGenerator.h"
#include "bb/NormalDistributionGenerator.h"
#include "bb/UniformDistributionGenerator.h"

#include "bb/Runner.h"
#include "bb/LoadMnist.h"
#include "bb/LoadCifar10.h"



#ifdef BB_WITH_CUDA
#include "bbcu/bbcu.h"
#include "bbcu/bbcu_util.h"
#endif



// ---------------------------------
//  type definition
// ---------------------------------


// container
using Tensor                            = bb::Tensor;
using FrameBuffer                       = bb::FrameBuffer;
using Variables                         = bb::Variables;


// model
using Model                             = bb::Model;
using Sequential                        = bb::Sequential;

using BinaryModulation_fp32             = bb::BinaryModulation<float, float>;
using BinaryModulation_bit              = bb::BinaryModulation<bb::Bit, float>;
using RealToBinary_fp32                 = bb::RealToBinary<float, float>;
using RealToBinary_bit                  = bb::RealToBinary<bb::Bit, float>;
using BinaryToReal_fp32                 = bb::BinaryToReal<float, float>;
using BinaryToReal_bit                  = bb::BinaryToReal<bb::Bit, float>;
using BitEncode_fp32                    = bb::BitEncode<float, float>;
using BitEncode_bit                     = bb::BitEncode<bb::Bit, float>;
using Reduce_fp32                       = bb::Reduce<float, float>; 
using Reduce_bit                        = bb::Reduce<bb::Bit, float>; 

using DenseAffine                       = bb::DenseAffine<float>;
using DepthwiseDenseAffine              = bb::DepthwiseDenseAffine<float>;

using SparseModel                       = bb::SparseModel;

using BinaryLutModel                    = bb::BinaryLutModel;
                                       
using BinaryLut2_fp32                   = bb::BinaryLutN<2, float, float>;
using BinaryLut2_bit                    = bb::BinaryLutN<2, bb::Bit, float>;
using BinaryLut4_fp32                   = bb::BinaryLutN<4, float, float>;
using BinaryLut4_bit                    = bb::BinaryLutN<4, bb::Bit, float>;
using BinaryLut5_fp32                   = bb::BinaryLutN<5, float, float>;
using BinaryLut5_bit                    = bb::BinaryLutN<5, bb::Bit, float>;
using BinaryLut6_fp32                   = bb::BinaryLutN<6, float, float>;
using BinaryLut6_bit                    = bb::BinaryLutN<6, bb::Bit, float>;
                                        
using StochasticLutModel                = bb::StochasticLutModel;

using StochasticLut2_fp32               = bb::StochasticLutN<2, float, float>;
using StochasticLut2_bit                = bb::StochasticLutN<2, bb::Bit, float>;
using StochasticLut4_fp32               = bb::StochasticLutN<4, float, float>;
using StochasticLut4_bit                = bb::StochasticLutN<4, bb::Bit, float>;
using StochasticLut5_fp32               = bb::StochasticLutN<5, float, float>;
using StochasticLut5_bit                = bb::StochasticLutN<5, bb::Bit, float>;
using StochasticLut6_fp32               = bb::StochasticLutN<6, float, float>;
using StochasticLut6_bit                = bb::StochasticLutN<6, bb::Bit, float>;
                                        
using DifferentiableLut2_fp32           = bb::DifferentiableLutN<2, float, float>;
using DifferentiableLut2_bit            = bb::DifferentiableLutN<2, bb::Bit, float>;
using DifferentiableLut4_fp32           = bb::DifferentiableLutN<4, float, float>;
using DifferentiableLut4_bit            = bb::DifferentiableLutN<4, bb::Bit, float>;
using DifferentiableLut5_fp32           = bb::DifferentiableLutN<5, float, float>;
using DifferentiableLut5_bit            = bb::DifferentiableLutN<5, bb::Bit, float>;
using DifferentiableLut6_fp32           = bb::DifferentiableLutN<6, float, float>;
using DifferentiableLut6_bit            = bb::DifferentiableLutN<6, bb::Bit, float>;

using DifferentiableLutDiscrete2_fp32   = bb::DifferentiableLutDiscreteN<2, float, float>;
using DifferentiableLutDiscrete2_bit    = bb::DifferentiableLutDiscreteN<2, bb::Bit, float>;
using DifferentiableLutDiscrete4_fp32   = bb::DifferentiableLutDiscreteN<4, float, float>;
using DifferentiableLutDiscrete4_bit    = bb::DifferentiableLutDiscreteN<4, bb::Bit, float>;
using DifferentiableLutDiscrete5_fp32   = bb::DifferentiableLutDiscreteN<5, float, float>;
using DifferentiableLutDiscrete5_bit    = bb::DifferentiableLutDiscreteN<5, bb::Bit, float>;
using DifferentiableLutDiscrete6_fp32   = bb::DifferentiableLutDiscreteN<6, float, float>;
using DifferentiableLutDiscrete6_bit    = bb::DifferentiableLutDiscreteN<6, bb::Bit, float>;
                                     
using MicroMlp4_16_fp32                 = bb::MicroMlp<4, 16, float, float>;
using MicroMlp4_16_bit                  = bb::MicroMlp<4, 16, bb::Bit, float>;
using MicroMlp5_16_fp32                 = bb::MicroMlp<5, 16, float, float>;
using MicroMlp5_16_bit                  = bb::MicroMlp<5, 16, bb::Bit, float>;
using MicroMlp6_16_fp32                 = bb::MicroMlp<6, 16, float, float>;
using MicroMlp6_16_bit                  = bb::MicroMlp<6, 16, bb::Bit, float>;


using Filter2d                          = bb::Filter2d;

using ConvolutionCol2Im_fp32            = bb::ConvolutionCol2Im <float, float>;
using ConvolutionCol2Im_bit             = bb::ConvolutionCol2Im <bb::Bit, float>;
using ConvolutionIm2Col_fp32            = bb::ConvolutionIm2Col <float, float>;
using ConvolutionIm2Col_bit             = bb::ConvolutionIm2Col <bb::Bit, float>;
using Convolution2d_fp32                = bb::Convolution2d<float, float>;
using Convolution2d_bit                 = bb::Convolution2d<bb::Bit, float>;

using MaxPooling_fp32                   = bb::MaxPooling<float, float>;
using MaxPooling_bit                    = bb::MaxPooling<bb::Bit, float>;

using StochasticMaxPooling_fp32         = bb::StochasticMaxPooling<float, float>;
using StochasticMaxPooling_bit          = bb::StochasticMaxPooling<bb::Bit, float>;
using StochasticMaxPooling2x2_fp32      = bb::StochasticMaxPooling2x2<float, float>;
using StochasticMaxPooling2x2_bit       = bb::StochasticMaxPooling2x2<bb::Bit, float>;

using UpSampling_fp32                   = bb::UpSampling<float, float>;
using UpSampling_bit                    = bb::UpSampling<bb::Bit, float>;

using Activation                        = bb::Activation;
using Binarize_fp32                     = bb::Binarize<float, float>;
using Binarize_bit                      = bb::Binarize<bb::Bit, float>;
using Sigmoid                           = bb::Sigmoid<float>;
using ReLU                              = bb::ReLU<float, float>;
using HardTanh                          = bb::HardTanh<float, float>;

using BatchNormalization                = bb::BatchNormalization<float>;
using StochasticBatchNormalization      = bb::StochasticBatchNormalization<float>;
using Dropout_fp32                      = bb::Dropout<float, float>;
using Dropout_bit                       = bb::Dropout<bb::Bit, float>;
using Shuffle                           = bb::Shuffle;
                                        
using LossFunction                      = bb::LossFunction;
using LossMeanSquaredError              = bb::LossMeanSquaredError<float>;
using LossSoftmaxCrossEntropy           = bb::LossSoftmaxCrossEntropy<float>;
                                        
using MetricsFunction                   = bb::MetricsFunction;
using MetricsCategoricalAccuracy        = bb::MetricsCategoricalAccuracy<float>;
using MetricsMeanSquaredError           = bb::MetricsMeanSquaredError<float>;
                                        
using Optimizer                         = bb::Optimizer;
using OptimizerSgd                      = bb::OptimizerSgd<float>;
using OptimizerAdam                     = bb::OptimizerAdam<float>;
using OptimizerAdaGrad                  = bb::OptimizerAdaGrad<float>;
                                        
using ValueGenerator                    = bb::ValueGenerator<float>;
using NormalDistributionGenerator       = bb::NormalDistributionGenerator<float>;
using UniformDistributionGenerator      = bb::UniformDistributionGenerator<float>;

using TrainData                         = bb::TrainData<float>;
using LoadMnist                         = bb::LoadMnist<float>;
using LoadCifar10                       = bb::LoadCifar10<float>;

//using RunStatus                         = bb::RunStatus;
//using Runner                            = bb::Runner<float>;



// ---------------------------------
//  functions
// ---------------------------------

int GetDeviceCount(void)
{
#if BB_WITH_CUDA
    return bbcu_GetDeviceCount();
#else
    return 0;
#endif
}

void SetDevice(int device)
{
#if BB_WITH_CUDA
    bbcu_SetDevice(device);
#endif
}

std::string GetDevicePropertiesString(int device)
{
#if BB_WITH_CUDA
    return bbcu::GetDevicePropertiesString(device);
#else
    return "host only\n"
#endif
}


std::string MakeVerilog_LutLayers(std::string module_name, std::vector< std::shared_ptr< bb::Model > > layers)
{
    std::stringstream ss;
    bb::ExportVerilog_LutModels(ss, module_name, layers);
    return ss.str();
}


std::string MakeVerilog_LutConvLayers(std::string module_name, std::vector< std::shared_ptr< bb::Model > > layers)
{
    std::stringstream ss;
    bb::ExportVerilog_LutCnnLayersAxi4s(ss, module_name, layers);
    return ss.str();
}






//////////////////////////////////////]
// PyBind11 module
//////////////////////////////////////]

namespace py = pybind11;
PYBIND11_MODULE(core, m) {
    m.doc() = "BinaryBrain ver " + bb::GetVersionString();

    // ------------------------------------
    //  Attribute
    // ------------------------------------

    m.attr("__version__") = py::cast(BB_VERSION);

    m.attr("TYPE_BIT")    = BB_TYPE_BIT;
    m.attr("TYPE_BINARY") = BB_TYPE_BINARY;
    m.attr("TYPE_FP16")   = BB_TYPE_FP16;
    m.attr("TYPE_FP32")   = BB_TYPE_FP32;
    m.attr("TYPE_FP64")   = BB_TYPE_FP64;
    m.attr("TYPE_INT8")   = BB_TYPE_INT8;
    m.attr("TYPE_INT16")  = BB_TYPE_INT16;
    m.attr("TYPE_INT32")  = BB_TYPE_INT32;
    m.attr("TYPE_INT64")  = BB_TYPE_INT64;
    m.attr("TYPE_UINT8")  = BB_TYPE_UINT8;
    m.attr("TYPE_UINT16") = BB_TYPE_UINT16;
    m.attr("TYPE_UINT32") = BB_TYPE_UINT32;
    m.attr("TYPE_UINT64") = BB_TYPE_UINT64;

    /*
    m.attr("BB_BORDER_CONSTANT")    = BB_BORDER_CONSTANT;
    m.attr("BB_BORDER_CONSTANT")    = BB_BORDER_CONSTANT;
    m.attr("BB_BORDER_REFLECT")     = BB_BORDER_REFLECT;
    m.attr("BB_BORDER_REFLECT_101") = BB_BORDER_REFLECT_101;
    m.attr("BB_BORDER_REPLICATE")   = BB_BORDER_REPLICATE;
    m.attr("BB_BORDER_WRAP")        = BB_BORDER_WRAP;
    */
    
    m.def("dtype_get_bit_size", &bb::DataType_GetBitSize);
    m.def("dtype_get_byte_size", &bb::DataType_GetByteSize);
    

    // ------------------------------------
    //  Container
    // ------------------------------------

    // Tensor
    py::class_< Tensor >(m, "Tensor")
        .def(py::init< bb::indices_t, int, bool >(),
            py::arg("shape"),
            py::arg("type")=BB_TYPE_FP32,
            py::arg("host_only")=false)
        .def("is_host_only", &Tensor::IsHostOnly)
        .def("get_type", &Tensor::GetType)
        .def("get_shape", &Tensor::GetShape)
        .def(py::self + py::self)
        .def(py::self + double())
        .def(double() + py::self)
        .def(py::self - py::self)
        .def(py::self - double())
        .def(double() - py::self)
        .def(py::self * py::self)
        .def(py::self * double())
        .def(double() * py::self)
        .def(py::self / py::self)
        .def(py::self / double())
        .def(double() / py::self)
        .def(py::self += py::self)
        .def(py::self += double())
        .def(py::self -= py::self)
        .def(py::self -= double())
        .def(py::self *= py::self)
        .def(py::self *= double())
        .def(py::self /= py::self)
        .def(py::self /= double())
        .def("numpy_int8",   &Tensor::Numpy<std::int8_t>)
        .def("numpy_int16",  &Tensor::Numpy<std::int16_t>)
        .def("numpy_int32",  &Tensor::Numpy<std::int32_t>)
        .def("numpy_int64",  &Tensor::Numpy<std::int64_t>)
        .def("numpy_uint8",  &Tensor::Numpy<std::int8_t>)
        .def("numpy_uint16", &Tensor::Numpy<std::uint16_t>)
        .def("numpy_uint32", &Tensor::Numpy<std::uint32_t>)
        .def("numpy_uint64", &Tensor::Numpy<std::uint64_t>)
        .def("numpy_fp32",   &Tensor::Numpy<float>)
        .def("numpy_fp64",   &Tensor::Numpy<double>)
        .def_static("from_numpy_int8",   &Tensor::FromNumpy<std::int8_t>)
        .def_static("from_numpy_int16",  &Tensor::FromNumpy<std::int16_t>)
        .def_static("from_numpy_int32",  &Tensor::FromNumpy<std::int32_t>)
        .def_static("from_numpy_int64",  &Tensor::FromNumpy<std::int64_t>)
        .def_static("from_numpy_uint8",  &Tensor::FromNumpy<std::uint8_t>)
        .def_static("from_numpy_uint16", &Tensor::FromNumpy<std::uint16_t>)
        .def_static("from_numpy_uint32", &Tensor::FromNumpy<std::uint32_t>)
        .def_static("from_numpy_uint64", &Tensor::FromNumpy<std::uint64_t>)
        .def_static("from_numpy_fp32",   &Tensor::FromNumpy<float>)
        .def_static("from_numpy_fp64",   &Tensor::FromNumpy<double>)
        ;

    // FrameBuffer
    py::class_< FrameBuffer >(m, "FrameBuffer")
        .def(py::init< bb::index_t, bb::indices_t, int, bool>(),
            py::arg("frame_size") = 0,
            py::arg("shape") = bb::indices_t(),
            py::arg("data_type") = 0,
            py::arg("host_only") = false)
    
        .def("resize",  (void (FrameBuffer::*)(bb::index_t, bb::indices_t, int))&bb::FrameBuffer::Resize,
                py::arg("frame_size"),
                py::arg("shape"),
                py::arg("data_type") = BB_TYPE_FP32)
        .def("is_host_only", &FrameBuffer::IsHostOnly)
        .def("get_type", &FrameBuffer::GetType)
        .def("get_frame_size", &FrameBuffer::GetFrameSize)
        .def("get_frame_stride", &FrameBuffer::GetFrameStride)
        .def("get_node_size", &FrameBuffer::GetNodeSize)
        .def("get_node_shape", &FrameBuffer::GetShape)
        .def("range", &FrameBuffer::Range)
        .def("concatenate", &FrameBuffer::Concatenate)
        .def(py::self + py::self)
        .def(py::self + double())
        .def(double() + py::self)
        .def(py::self - py::self)
        .def(py::self - double())
        .def(double() - py::self)
        .def(py::self * py::self)
        .def(py::self * double())
        .def(double() * py::self)
        .def(py::self / py::self)
        .def(py::self / double())
        .def(double() / py::self)
        .def(py::self += py::self)
        .def(py::self += double())
        .def(py::self -= py::self)
        .def(py::self -= double())
        .def(py::self *= py::self)
        .def(py::self *= double())
        .def(py::self /= py::self)
        .def(py::self /= double())
        .def("numpy_int8",   &FrameBuffer::Numpy<std::int8_t>)
        .def("numpy_int16",  &FrameBuffer::Numpy<std::int16_t>)
        .def("numpy_int32",  &FrameBuffer::Numpy<std::int32_t>)
        .def("numpy_int64",  &FrameBuffer::Numpy<std::int64_t>)
        .def("numpy_uint8",  &FrameBuffer::Numpy<std::int8_t>)
        .def("numpy_uint16", &FrameBuffer::Numpy<std::uint16_t>)
        .def("numpy_uint32", &FrameBuffer::Numpy<std::uint32_t>)
        .def("numpy_uint64", &FrameBuffer::Numpy<std::uint64_t>)
        .def("numpy_fp32",   &FrameBuffer::Numpy<float>)
        .def("numpy_fp64",   &FrameBuffer::Numpy<double>)
        .def_static("from_numpy_int8",   &FrameBuffer::FromNumpy<std::int8_t>)
        .def_static("from_numpy_int16",  &FrameBuffer::FromNumpy<std::int16_t>)
        .def_static("from_numpy_int32",  &FrameBuffer::FromNumpy<std::int32_t>)
        .def_static("from_numpy_int64",  &FrameBuffer::FromNumpy<std::int64_t>)
        .def_static("from_numpy_uint8",  &FrameBuffer::FromNumpy<std::uint8_t>)
        .def_static("from_numpy_uint16", &FrameBuffer::FromNumpy<std::uint16_t>)
        .def_static("from_numpy_uint32", &FrameBuffer::FromNumpy<std::uint32_t>)
        .def_static("from_numpy_uint64", &FrameBuffer::FromNumpy<std::uint64_t>)
        .def_static("from_numpy_fp32",   &FrameBuffer::FromNumpy<float>)
        .def_static("from_numpy_fp64",   &FrameBuffer::FromNumpy<double>)
        .def_static("calc_frame_stride", &FrameBuffer::CalcFrameStride)
        ;
    
    // Variables
    py::class_< Variables, std::shared_ptr<Variables> >(m, "Variables")
        .def(py::init<>())
        .def("push_back", (void (Variables::*)(Variables const &))&Variables::PushBack)
        ;



    // ------------------------------------
    //  Models
    // ------------------------------------
    
    // model
    py::class_< Model, std::shared_ptr<Model> >(m, "Model")
        .def("get_name", &Model::GetName)
        .def("set_name", &Model::SetName)
        .def("is_named", &Model::IsNamed)
        .def("get_class_name", &Model::GetClassName)
        .def("get_info", &Model::GetInfoString,
                py::arg("depth")    = 0,
                py::arg("columns")  = 70,
                py::arg("nest")     = 0)
        .def("send_command",  &Model::SendCommand, "SendCommand",
                py::arg("command"),
                py::arg("send_to") = "all")
        .def("get_input_shape", &Model::GetInputShape)
        .def("set_input_shape", &Model::SetInputShape)
        .def("get_output_shape", &Model::GetOutputShape)
        .def("get_input_node_size", &Model::GetInputNodeSize)
        .def("get_output_node_size", &Model::GetOutputNodeSize)
        .def("get_parameters", &Model::GetParameters)
        .def("get_gradients", &Model::GetGradients)
        .def("forward_node",  &Model::ForwardNode)
        .def("forward",  &Model::Forward)
        .def("backward", &Model::Backward)
        .def("dump", &Model::DumpBytes)
        .def("load", &Model::LoadBytes)
        .def("save_binary", &Model::SaveBinary)
        .def("load_binary", &Model::LoadBinary)
        .def("save_json", &Model::SaveJson)
        .def("load_json", &Model::LoadJson);
    

    py::class_< Sequential, Model, std::shared_ptr<Sequential> >(m, "Sequential")
        .def_static("create",   &Sequential::Create)
        .def("add",             &Sequential::Add)
        ;


    py::class_< BitEncode_fp32, Model, std::shared_ptr<BitEncode_fp32> >(m, "BitEncode_fp32")
        .def_static("create",   &BitEncode_fp32::CreateEx);
    py::class_< BitEncode_bit, Model, std::shared_ptr<BitEncode_bit> >(m, "BitEncode_bit")
        .def_static("create",   &BitEncode_fp32::CreateEx);
    

    py::class_< Shuffle, Model, std::shared_ptr<Shuffle> >(m, "Shuffle")
        .def_static("create",   &Shuffle::CreateEx);
    
    py::class_< BinaryModulation_fp32, Model, std::shared_ptr<BinaryModulation_fp32> >(m, "BinaryModulation_fp32")
        .def_static("create", &BinaryModulation_fp32::CreateEx,
                py::arg("layer"),
                py::arg("output_shape")              = bb::indices_t(),
                py::arg("depth_modulation_size")     = 1,
                py::arg("training_modulation_size")  = 1,
                py::arg("training_value_generator")  = nullptr,
                py::arg("training_framewise")        = true,
                py::arg("training_input_range_lo")   = 0.0f,
                py::arg("training_input_range_hi")   = 1.0f,
                py::arg("inference_modulation_size") = -1,
                py::arg("inference_value_generator") = nullptr,
                py::arg("inference_framewise")       = true,
                py::arg("inference_input_range_lo")  = 0.0f,
                py::arg("inference_input_range_hi")  = 1.0f);

    py::class_< BinaryModulation_bit, Model, std::shared_ptr<BinaryModulation_bit> >(m, "BinaryModulation_bit")
        .def_static("create", &BinaryModulation_bit::CreateEx,
                py::arg("layer"),
                py::arg("output_shape")              = bb::indices_t(),
                py::arg("depth_modulation_size")     = 1,
                py::arg("training_modulation_size")  = 1,
                py::arg("training_value_generator")  = nullptr,
                py::arg("training_framewise")        = true,
                py::arg("training_input_range_lo")   = 0.0f,
                py::arg("training_input_range_hi")   = 1.0f,
                py::arg("inference_modulation_size") = -1,
                py::arg("inference_value_generator") = nullptr,
                py::arg("inference_framewise")       = true,
                py::arg("inference_input_range_lo")  = 0.0f,
                py::arg("inference_input_range_hi")  = 1.0f);

    py::class_< RealToBinary_fp32, Model, std::shared_ptr<RealToBinary_fp32> >(m, "RealToBinary_fp32")
        .def_static("create", &RealToBinary_fp32::CreateEx,
                py::arg("frame_modulation_size") = 1,
                py::arg("depth_modulation_size") = 1,
                py::arg("value_generator")  = nullptr,
                py::arg("framewise")        = false,
                py::arg("input_range_lo")   = 0.0f,
                py::arg("input_range_hi")   = 1.0f);

    py::class_< RealToBinary_bit, Model, std::shared_ptr<RealToBinary_bit> >(m, "RealToBinary_bit")
        .def_static("create", &RealToBinary_bit::CreateEx,
                py::arg("frame_modulation_size") = 1,
                py::arg("depth_modulation_size") = 1,
                py::arg("value_generator")  = nullptr,
                py::arg("framewise")        = false,
                py::arg("input_range_lo")   = 0.0f,
                py::arg("input_range_hi")   = 1.0f);

    py::class_< BinaryToReal_fp32, Model, std::shared_ptr<BinaryToReal_fp32> >(m, "BinaryToReal_fp32")
        .def_static("create", &BinaryToReal_fp32::CreateEx,
                py::arg("frame_modulation_size") = 1,
                py::arg("output_shape")          = bb::indices_t());

    py::class_< BinaryToReal_bit, Model, std::shared_ptr<BinaryToReal_bit> >(m, "BinaryToReal_bit")
        .def_static("create", &BinaryToReal_bit::CreateEx,
                py::arg("frame_modulation_size") = 1,
                py::arg("output_shape")          = bb::indices_t());

    py::class_< Reduce_fp32, Model, std::shared_ptr<Reduce_fp32> >(m, "Reduce_fp32")
        .def_static("create",   &Reduce_fp32::CreateEx);
    py::class_< Reduce_bit, Model, std::shared_ptr<Reduce_bit> >(m, "Reduce_bit")
        .def_static("create",   &Reduce_bit::CreateEx);

    // DenseAffine
    py::class_< DenseAffine, Model, std::shared_ptr<DenseAffine> >(m, "DenseAffine")
        .def_static("create",   &DenseAffine::CreateEx, "create",
            py::arg("output_shape"),
            py::arg("initialize_std") = 0.01f,
            py::arg("initializer")    = "he",
            py::arg("seed")           = 1)
        .def("W", ((Tensor& (DenseAffine::*)())&DenseAffine::W))
        .def("b", ((Tensor& (DenseAffine::*)())&DenseAffine::b))
        .def("dW", ((Tensor& (DenseAffine::*)())&DenseAffine::dW))
        .def("db", ((Tensor& (DenseAffine::*)())&DenseAffine::db));
    
    // DepthwiseDenseAffine
    py::class_< DepthwiseDenseAffine, Model, std::shared_ptr<DepthwiseDenseAffine> >(m, "DepthwiseDenseAffine")
        .def_static("create",   &DepthwiseDenseAffine::CreateEx, "create",
            py::arg("output_shape"),
            py::arg("input_point_size")=0,
            py::arg("depth_size")=0,
            py::arg("initialize_std") = 0.01f,
            py::arg("initializer")    = "he",
            py::arg("seed")           = 1)
        .def("W", ((Tensor& (DepthwiseDenseAffine::*)())&DepthwiseDenseAffine::W))
        .def("b", ((Tensor& (DepthwiseDenseAffine::*)())&DepthwiseDenseAffine::b))
        .def("dW", ((Tensor& (DepthwiseDenseAffine::*)())&DepthwiseDenseAffine::dW))
        .def("db", ((Tensor& (DepthwiseDenseAffine::*)())&DepthwiseDenseAffine::db));


    // SparseModel
    py::class_< SparseModel, Model, std::shared_ptr<SparseModel> >(m, "SparseModel")
        .def("get_connection_size", &SparseModel::GetConnectionSize)
        .def("set_connection", &SparseModel::SetConnectionIndices)
        .def("get_connection", &SparseModel::GetConnectionIndices)
        .def("set_connection_index", &SparseModel::SetConnectionIndex)
        .def("get_connection_index", &SparseModel::GetConnectionIndex)
        .def("get_node_connection_size", &SparseModel::GetNodeConnectionSize)
        .def("set_node_connection_index", &SparseModel::SetNodeConnectionIndex)
        .def("get_node_connection_index", &SparseModel::GetNodeConnectionIndex)
        .def("get_lut_table_size", &SparseModel::GetLutTableSize)
        .def("get_lut_table", &SparseModel::GetLutTable)
        ;

    // BinaryLUT
    py::class_< BinaryLutModel, SparseModel, std::shared_ptr<BinaryLutModel> >(m, "BinaryLutModel")
        .def("get_lut_table_size", &BinaryLutModel::GetLutTableSize)
        .def("get_lut_table", &BinaryLutModel::GetLutTable)
        .def("set_lut_table", &BinaryLutModel::SetLutTable)
        .def("import_layer", &BinaryLutModel::ImportLayer);

    py::class_< BinaryLut6_fp32, BinaryLutModel, std::shared_ptr<BinaryLut6_fp32> >(m, "BinaryLut6_fp32")
        .def_static("create", &BinaryLut6_fp32::CreatePy);
    py::class_< BinaryLut5_fp32, BinaryLutModel, std::shared_ptr<BinaryLut5_fp32> >(m, "BinaryLut5_fp32")
        .def_static("create", &BinaryLut5_fp32::CreatePy);
    py::class_< BinaryLut4_fp32, BinaryLutModel, std::shared_ptr<BinaryLut4_fp32> >(m, "BinaryLut4_fp32")
        .def_static("create", &BinaryLut4_fp32::CreatePy);
    py::class_< BinaryLut2_fp32, BinaryLutModel, std::shared_ptr<BinaryLut2_fp32> >(m, "BinaryLut2_fp32")
        .def_static("create", &BinaryLut2_fp32::CreatePy);
    py::class_< BinaryLut6_bit, BinaryLutModel, std::shared_ptr<BinaryLut6_bit> >(m, "BinaryLut6_bit")
        .def_static("create", &BinaryLut6_bit::CreatePy);
    py::class_< BinaryLut5_bit, BinaryLutModel, std::shared_ptr<BinaryLut5_bit> >(m, "BinaryLut5_bit")
        .def_static("create", &BinaryLut5_bit::CreatePy);
    py::class_< BinaryLut4_bit, BinaryLutModel, std::shared_ptr<BinaryLut4_bit> >(m, "BinaryLut4_bit")
        .def_static("create", &BinaryLut4_bit::CreatePy);
    py::class_< BinaryLut2_bit, BinaryLutModel, std::shared_ptr<BinaryLut2_bit> >(m, "BinaryLut2_bit")
        .def_static("create", &BinaryLut2_bit::CreatePy);


    // StochasticLutModel
    py::class_< StochasticLutModel, SparseModel, std::shared_ptr<StochasticLutModel> >(m, "StochasticLutModel")
        .def("W",  ((Tensor& (StochasticLutModel::*)())&StochasticLutModel::W))
        .def("dW", ((Tensor& (StochasticLutModel::*)())&StochasticLutModel::dW));

    // StochasticLut
    py::class_< StochasticLut6_fp32, StochasticLutModel, std::shared_ptr<StochasticLut6_fp32> >(m, "StochasticLut6_fp32")
        .def_static("create", &StochasticLut6_fp32::CreateEx, "create StochasticLut6_fp32");
    py::class_< StochasticLut5_fp32, StochasticLutModel, std::shared_ptr<StochasticLut5_fp32> >(m, "StochasticLut5_fp32")
        .def_static("create", &StochasticLut5_fp32::CreateEx, "create StochasticLut6_fp32");
    py::class_< StochasticLut4_fp32, StochasticLutModel, std::shared_ptr<StochasticLut4_fp32> >(m, "StochasticLut4_fp32")
        .def_static("create", &StochasticLut4_fp32::CreateEx, "create StochasticLut6_fp32");
    py::class_< StochasticLut2_fp32, StochasticLutModel, std::shared_ptr<StochasticLut2_fp32> >(m, "StochasticLut2_fp32")
        .def_static("create", &StochasticLut2_fp32::CreateEx, "create StochasticLut6_fp32");

    py::class_< StochasticLut6_bit, StochasticLutModel, std::shared_ptr<StochasticLut6_bit> >(m, "StochasticLut6_bit")
        .def_static("create", &StochasticLut6_bit::CreateEx, "create StochasticLut6_bit");
    py::class_< StochasticLut5_bit, StochasticLutModel, std::shared_ptr<StochasticLut5_bit> >(m, "StochasticLut5_bit")
        .def_static("create", &StochasticLut5_bit::CreateEx, "create StochasticLut6_bit");
    py::class_< StochasticLut4_bit, StochasticLutModel, std::shared_ptr<StochasticLut4_bit> >(m, "StochasticLut4_bit")
        .def_static("create", &StochasticLut4_bit::CreateEx, "create StochasticLut6_bit");
    py::class_< StochasticLut2_bit, StochasticLutModel, std::shared_ptr<StochasticLut2_bit> >(m, "StochasticLut2_bit")
        .def_static("create", &StochasticLut2_bit::CreateEx, "create StochasticLut6_bit");


    // DifferentiableLut
    py::class_< DifferentiableLut6_fp32, StochasticLutModel, std::shared_ptr<DifferentiableLut6_fp32> >(m, "DifferentiableLut6_fp32")
        .def_static("create", &DifferentiableLut6_fp32::CreatePy, "create DifferentiableLut6_fp32");
    py::class_< DifferentiableLut5_fp32, StochasticLutModel, std::shared_ptr<DifferentiableLut5_fp32> >(m, "DifferentiableLut5_fp32")
        .def_static("create", &DifferentiableLut5_fp32::CreatePy, "create DifferentiableLut5_fp32");
    py::class_< DifferentiableLut4_fp32, StochasticLutModel, std::shared_ptr<DifferentiableLut4_fp32> >(m, "DifferentiableLut4_fp32")
        .def_static("create", &DifferentiableLut4_fp32::CreatePy, "create DifferentiableLut4_fp32");
    py::class_< DifferentiableLut2_fp32, StochasticLutModel, std::shared_ptr<DifferentiableLut2_fp32> >(m, "DifferentiableLut2_fp32")
        .def_static("create", &DifferentiableLut2_fp32::CreatePy, "create DifferentiableLut2_fp32");

    py::class_< DifferentiableLut6_bit, StochasticLutModel, std::shared_ptr<DifferentiableLut6_bit> >(m, "DifferentiableLut6_bit")
        .def_static("create", &DifferentiableLut6_bit::CreatePy, "create DifferentiableLut6_bit");
    py::class_< DifferentiableLut5_bit, StochasticLutModel, std::shared_ptr<DifferentiableLut5_bit> >(m, "DifferentiableLut5_bit")
        .def_static("create", &DifferentiableLut5_bit::CreatePy, "create DifferentiableLut5_bit");
    py::class_< DifferentiableLut4_bit, StochasticLutModel, std::shared_ptr<DifferentiableLut4_bit> >(m, "DifferentiableLut4_bit")
        .def_static("create", &DifferentiableLut4_bit::CreatePy, "create DifferentiableLut4_bit");
    py::class_< DifferentiableLut2_bit, StochasticLutModel, std::shared_ptr<DifferentiableLut2_bit> >(m, "DifferentiableLut2_bit")
        .def_static("create", &DifferentiableLut2_bit::CreatePy, "create DifferentiableLut2_bit");

   // DifferentiableLutDiscrete
    py::class_< DifferentiableLutDiscrete6_fp32, StochasticLutModel, std::shared_ptr<DifferentiableLutDiscrete6_fp32> >(m, "DifferentiableLutDiscrete6_fp32")
        .def_static("create", &DifferentiableLutDiscrete6_fp32::CreatePy, "create DifferentiableLutDiscrete6_fp32");
    py::class_< DifferentiableLutDiscrete5_fp32, StochasticLutModel, std::shared_ptr<DifferentiableLutDiscrete5_fp32> >(m, "DifferentiableLutDiscrete5_fp32")
        .def_static("create", &DifferentiableLutDiscrete5_fp32::CreatePy, "create DifferentiableLutDiscrete5_fp32");
    py::class_< DifferentiableLutDiscrete4_fp32, StochasticLutModel, std::shared_ptr<DifferentiableLutDiscrete4_fp32> >(m, "DifferentiableLutDiscrete4_fp32")
        .def_static("create", &DifferentiableLutDiscrete4_fp32::CreatePy, "create DifferentiableLutDiscrete4_fp32");
    py::class_< DifferentiableLutDiscrete2_fp32, StochasticLutModel, std::shared_ptr<DifferentiableLutDiscrete2_fp32> >(m, "DifferentiableLutDiscrete2_fp32")
        .def_static("create", &DifferentiableLutDiscrete2_fp32::CreatePy, "create DifferentiableLutDiscrete2_fp32");

    py::class_< DifferentiableLutDiscrete6_bit, StochasticLutModel, std::shared_ptr<DifferentiableLutDiscrete6_bit> >(m, "DifferentiableLutDiscrete6_bit")
        .def_static("create", &DifferentiableLutDiscrete6_bit::CreatePy, "create DifferentiableLutDiscrete6_bit");
    py::class_< DifferentiableLutDiscrete5_bit, StochasticLutModel, std::shared_ptr<DifferentiableLutDiscrete5_bit> >(m, "DifferentiableLutDiscrete5_bit")
        .def_static("create", &DifferentiableLutDiscrete5_bit::CreatePy, "create DifferentiableLutDiscrete5_bit");
    py::class_< DifferentiableLutDiscrete4_bit, StochasticLutModel, std::shared_ptr<DifferentiableLutDiscrete4_bit> >(m, "DifferentiableLutDiscrete4_bit")
        .def_static("create", &DifferentiableLutDiscrete4_bit::CreatePy, "create DifferentiableLutDiscrete4_bit");
    py::class_< DifferentiableLutDiscrete2_bit, StochasticLutModel, std::shared_ptr<DifferentiableLutDiscrete2_bit> >(m, "DifferentiableLutDiscrete2_bit")
        .def_static("create", &DifferentiableLutDiscrete2_bit::CreatePy, "create DifferentiableLutDiscrete2_bit");

    // MicroMlp
    py::class_< MicroMlp6_16_fp32, SparseModel, std::shared_ptr<MicroMlp6_16_fp32> >(m, "MicroMlp6_16_fp32")
        .def_static("create", &MicroMlp6_16_fp32::CreatePy, "create MicroMlp6_16_fp32");
    py::class_< MicroMlp5_16_fp32, SparseModel, std::shared_ptr<MicroMlp5_16_fp32> >(m, "MicroMlp5_16_fp32")
        .def_static("create", &MicroMlp5_16_fp32::CreatePy, "create MicroMlp5_16_fp32");
    py::class_< MicroMlp4_16_fp32, SparseModel, std::shared_ptr<MicroMlp4_16_fp32> >(m, "MicroMlp4_16_fp32")
        .def_static("create", &MicroMlp4_16_fp32::CreatePy, "create MicroMlp4_16_fp32");

    py::class_< MicroMlp6_16_bit, SparseModel, std::shared_ptr<MicroMlp6_16_bit> >(m, "MicroMlp6_16_bit")
        .def_static("create", &MicroMlp6_16_bit::CreatePy, "create MicroMlp6_16_bit");
    py::class_< MicroMlp5_16_bit, SparseModel, std::shared_ptr<MicroMlp5_16_bit> >(m, "MicroMlp5_16_bit")
        .def_static("create", &MicroMlp5_16_bit::CreatePy, "create MicroMlp5_16_bit");
    py::class_< MicroMlp4_16_bit, SparseModel, std::shared_ptr<MicroMlp4_16_bit> >(m, "MicroMlp4_16_bit")
        .def_static("create", &MicroMlp4_16_bit::CreatePy, "create MicroMlp4_16_bit");


    // filter
    py::class_< Filter2d, Model, std::shared_ptr<Filter2d> >(m, "Filter2d");

    py::class_< ConvolutionIm2Col_fp32, Model, std::shared_ptr<ConvolutionIm2Col_fp32> >(m, "ConvolutionIm2Col_fp32")
        .def_static("create", &ConvolutionIm2Col_fp32::CreateEx)
        ;

    py::class_< ConvolutionIm2Col_bit, Model, std::shared_ptr<ConvolutionIm2Col_bit> >(m, "ConvolutionIm2Col_bit")
        .def_static("create", &ConvolutionIm2Col_bit::CreateEx)
        ;

    py::class_< ConvolutionCol2Im_fp32, Model, std::shared_ptr<ConvolutionCol2Im_fp32> >(m, "ConvolutionCol2Im_fp32")
        .def_static("create", &ConvolutionCol2Im_fp32::CreateEx)
        ;

    py::class_< ConvolutionCol2Im_bit, Model, std::shared_ptr<ConvolutionCol2Im_bit> >(m, "ConvolutionCol2Im_bit")
        .def_static("create", &ConvolutionCol2Im_bit::CreateEx)
        ;

    py::class_< Convolution2d_fp32, Filter2d, std::shared_ptr<Convolution2d_fp32> >(m, "Convolution2d_fp32")
        .def_static("create", &Convolution2d_fp32::CreatePy)
        .def("get_sub_layer", &Convolution2d_fp32::GetSubLayer)
        ;

    py::class_< Convolution2d_bit, Filter2d, std::shared_ptr<Convolution2d_bit> >(m, "Convolution2d_bit")
        .def_static("create", &Convolution2d_bit::CreatePy)
        .def("get_sub_layer", &Convolution2d_bit::GetSubLayer)
        ;

    py::class_< MaxPooling_fp32, Filter2d, std::shared_ptr<MaxPooling_fp32> >(m, "MaxPooling_fp32")
        .def_static("create", &MaxPooling_fp32::CreatePy);
    py::class_< MaxPooling_bit, Filter2d, std::shared_ptr<MaxPooling_bit> >(m, "MaxPooling_bit")
        .def_static("create", &MaxPooling_bit::CreatePy);

    py::class_< StochasticMaxPooling_fp32, Filter2d, std::shared_ptr<StochasticMaxPooling_fp32> >(m, "StochasticMaxPooling_fp32")
        .def_static("create", &StochasticMaxPooling_fp32::Create);
    py::class_< StochasticMaxPooling_bit, Filter2d, std::shared_ptr<StochasticMaxPooling_bit> >(m, "StochasticMaxPooling_bit")
        .def_static("create", &StochasticMaxPooling_bit::Create);

    py::class_< StochasticMaxPooling2x2_fp32, Filter2d, std::shared_ptr<StochasticMaxPooling2x2_fp32> >(m, "StochasticMaxPooling2x2_fp32")
        .def_static("create", &StochasticMaxPooling2x2_fp32::Create);
    py::class_< StochasticMaxPooling2x2_bit, Filter2d, std::shared_ptr<StochasticMaxPooling2x2_bit> >(m, "StochasticMaxPooling2x2_bit")
        .def_static("create", &StochasticMaxPooling2x2_bit::Create);

    py::class_< UpSampling_fp32, Model, std::shared_ptr<UpSampling_fp32> >(m, "UpSampling_fp32")
        .def_static("create", &UpSampling_fp32::CreatePy);
    py::class_< UpSampling_bit, Model, std::shared_ptr<UpSampling_bit> >(m, "UpSampling_bit")
        .def_static("create", &UpSampling_bit::CreatePy);


    // activation
    py::class_< Activation, Model, std::shared_ptr<Activation> >(m, "Activation");

    py::class_< Binarize_fp32, Activation, std::shared_ptr<Binarize_fp32> >(m, "Binarize")
        .def_static("create", &Binarize_fp32::CreateEx,
                py::arg("binary_th")    =  0.0f,
                py::arg("hardtanh_min") = -1.0f,
                py::arg("hardtanh_max") = +1.0f);
    
    py::class_< Binarize_bit, Activation, std::shared_ptr<Binarize_bit> >(m, "Binarize_bit")
        .def_static("create", &Binarize_bit::CreateEx,
                py::arg("binary_th")    =  0.0f,
                py::arg("hardtanh_min") = -1.0f,
                py::arg("hardtanh_max") = +1.0f);

    py::class_< Sigmoid, Binarize_fp32, std::shared_ptr<Sigmoid> >(m, "Sigmoid")
        .def_static("create",   &Sigmoid::Create);

    py::class_< ReLU, Binarize_fp32, std::shared_ptr<ReLU> >(m, "ReLU")
        .def_static("create",   &ReLU::Create);

    py::class_< HardTanh, Binarize_fp32, std::shared_ptr<HardTanh> >(m, "HardTanh")
        .def_static("create", &HardTanh::CreateEx,
                py::arg("hardtanh_min") = -1.0,
                py::arg("hardtanh_max") = +1.0);

    
    py::class_< Dropout_fp32, Activation, std::shared_ptr<Dropout_fp32> >(m, "Dropout_fp32")
        .def_static("create", &Dropout_fp32::CreateEx,
                py::arg("rate") = 0.5,
                py::arg("seed") = 1);

    py::class_< Dropout_bit, Activation, std::shared_ptr<Dropout_bit> >(m, "Dropout_bit")
        .def_static("create", &Dropout_bit::CreateEx,
                py::arg("rate") = 0.5,
                py::arg("seed") = 1);

    py::class_< BatchNormalization, Activation, std::shared_ptr<BatchNormalization> >(m, "BatchNormalization")
        .def_static("create", &BatchNormalization::CreateEx,
                py::arg("momentum")  = 0.9f,
                py::arg("gamma")     = 1.0f,
                py::arg("beta")      = 0.0f,
                py::arg("fix_gamma") = false,
                py::arg("fix_beta")  = false);

    py::class_< StochasticBatchNormalization, Activation, std::shared_ptr<StochasticBatchNormalization> >(m, "StochasticBatchNormalization")
        .def_static("create", &StochasticBatchNormalization::CreateEx,
                py::arg("momentum")  = 0.9,
                py::arg("gamma")     = 0.2,
                py::arg("beta")      = 0.5);

    // Loss Functions
    py::class_< LossFunction, std::shared_ptr<LossFunction> >(m, "LossFunction")
        .def("clear",          &LossFunction::Clear)
        .def("get_loss",       &LossFunction::GetLoss)
        .def("calculate_loss", &LossFunction::CalculateLoss,
            py::arg("y_buf"),
            py::arg("t_buf"),
            py::arg("mini_batch_size"));

    py::class_< LossSoftmaxCrossEntropy, LossFunction, std::shared_ptr<LossSoftmaxCrossEntropy> >(m, "LossSoftmaxCrossEntropy")
        .def_static("create", &LossSoftmaxCrossEntropy::Create);

    py::class_< LossMeanSquaredError, LossFunction, std::shared_ptr<LossMeanSquaredError> >(m, "LossMeanSquaredError")
        .def_static("create", &LossMeanSquaredError::Create);


    // Metrics Functions
    py::class_< MetricsFunction, std::shared_ptr<MetricsFunction> >(m, "MetricsFunction")
        .def("clear",              &MetricsFunction::Clear)
        .def("get_metrics",        &MetricsFunction::GetMetrics)
        .def("calculate_metrics",  &MetricsFunction::CalculateMetrics)
        .def("get_metrics_string", &MetricsFunction::GetMetricsString);

    py::class_< MetricsCategoricalAccuracy, MetricsFunction, std::shared_ptr<MetricsCategoricalAccuracy> >(m, "MetricsCategoricalAccuracy")
        .def_static("create", &MetricsCategoricalAccuracy::Create);

    py::class_< MetricsMeanSquaredError, MetricsFunction, std::shared_ptr<MetricsMeanSquaredError> >(m, "MetricsMeanSquaredError")
        .def_static("create", &MetricsMeanSquaredError::Create);


    // Optimizer
    py::class_< Optimizer, std::shared_ptr<Optimizer> >(m, "Optimizer")
        .def("set_variables", &Optimizer::SetVariables)
        .def("update",        &Optimizer::Update);
    
    py::class_< OptimizerSgd, Optimizer, std::shared_ptr<OptimizerSgd> >(m, "OptimizerSgd")
        .def_static("create", (std::shared_ptr<OptimizerSgd> (*)(float))&OptimizerSgd::Create, "create",
            py::arg("learning_rate") = 0.01f);
    
    py::class_< OptimizerAdaGrad, Optimizer, std::shared_ptr<OptimizerAdaGrad> >(m, "OptimizerAdaGrad")
        .def_static("Create", (std::shared_ptr<OptimizerAdaGrad> (*)(float))&OptimizerAdaGrad::Create,
            py::arg("learning_rate") = 0.01f);

    py::class_< OptimizerAdam, Optimizer, std::shared_ptr<OptimizerAdam> >(m, "OptimizerAdam")
        .def_static("create", &OptimizerAdam::CreateEx,
            py::arg("learning_rate") = 0.001f,
            py::arg("beta1")         = 0.9f,
            py::arg("beta2")         = 0.999f); 
    
        
    // ValueGenerator
    py::class_< ValueGenerator, std::shared_ptr<ValueGenerator> >(m, "ValueGenerator");
    
    py::class_< NormalDistributionGenerator, ValueGenerator, std::shared_ptr<NormalDistributionGenerator> >(m, "NormalDistributionGenerator")
        .def_static("create", &NormalDistributionGenerator::Create,
            py::arg("mean")   = 0.0f,
            py::arg("stddev") = 1.0f,
            py::arg("seed")   = 1);
    
    py::class_< UniformDistributionGenerator, ValueGenerator, std::shared_ptr<UniformDistributionGenerator> >(m, "UniformDistributionGenerator")
        .def_static("Create", &UniformDistributionGenerator::Create,
            py::arg("a")    = 0.0f,
            py::arg("b")    = 1.0f,
            py::arg("seed") = 1);


    // TrainData
    py::class_< TrainData >(m, "TrainData")
        .def_readwrite("x_shape", &TrainData::x_shape)
        .def_readwrite("t_shape", &TrainData::t_shape)
        .def_readwrite("x_train", &TrainData::x_train)
        .def_readwrite("t_train", &TrainData::t_train)
        .def_readwrite("x_test",  &TrainData::x_test)
        .def_readwrite("t_test",  &TrainData::t_test)
        .def("empty", &TrainData::empty);

    // LoadMNIST
    py::class_< LoadMnist >(m, "LoadMnist")
        .def_static("load", &LoadMnist::Load,
            py::arg("max_train") = -1,
            py::arg("max_test")  = -1,
            py::arg("num_class") = 10);
    
    // LoadCifar10
    py::class_< LoadCifar10 >(m, "LoadCifar10")
        .def_static("load", &LoadCifar10::Load,
            py::arg("num") = 5);

    /*
    // RunStatus
    py::class_< RunStatus >(m, "RunStatus")
        .def_static("WriteJson", &RunStatus::WriteJson)
        .def_static("ReadJson",  &RunStatus::ReadJson);


    // Runnner
    py::class_< Runner, std::shared_ptr<Runner> >(m, "Runner")
        .def_static("create", &Runner::CreateEx,
            py::arg("name"),
            py::arg("net"),
            py::arg("lossFunc"),
            py::arg("metricsFunc"),
            py::arg("optimizer"),
            py::arg("max_run_size") = 0,
            py::arg("print_progress") = true,
            py::arg("print_progress_loss") = true,
            py::arg("print_progress_accuracy") = true,
            py::arg("log_write") = true,
            py::arg("log_append") = true,
            py::arg("file_read") = false,
            py::arg("file_write") = false,
            py::arg("write_serial") = false,
            py::arg("initial_evaluation") = false,
            py::arg("seed") = 1)
        .def("fitting", &Runner::Fitting,
            py::arg("td"),
            py::arg("epoch_size"),
            py::arg("batch_size"));
    */


    // ------------------------------------
    //  Others
    // ------------------------------------

    // version
    m.def("get_version_string", &bb::GetVersionString);

    // verilog
    m.def("make_verilog_lut_layers",     &MakeVerilog_LutLayers);
    m.def("make_verilog_lut_cnv_layers", &MakeVerilog_LutConvLayers);

    // OpenMP
    m.def("omp_set_num_threads", &omp_set_num_threads);

    // CUDA device
    py::class_< bb::Manager >(m, "Manager")
        .def_static("is_device_available", &bb::Manager::IsDeviceAvailable)
        .def_static("set_host_only", &bb::Manager::SetHostOnly);

    m.def("get_device_count",             &GetDeviceCount);
    m.def("set_device",                   &SetDevice,                 py::arg("device") = 0);
    m.def("get_device_properties_string", &GetDevicePropertiesString, py::arg("device") = 0);
}



// end of file
