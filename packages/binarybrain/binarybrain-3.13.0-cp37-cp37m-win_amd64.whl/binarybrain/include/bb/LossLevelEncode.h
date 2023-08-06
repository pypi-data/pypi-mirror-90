// --------------------------------------------------------------------------
//  Binary Brain  -- binary neural net framework
//
//                                Copyright (C) 2018-2020 by Ryuji Fuchikami
//                                https://github.com/ryuz
//                                ryuji.fuchikami@nifty.com
// --------------------------------------------------------------------------


#pragma once


#include <vector>
#include <cmath>


#include "bb/LossFunction.h"


namespace bb {

template <typename BinType = float, typename RealType = float>
class LossLevelEncode : public LossFunction
{
protected:
    FrameBuffer m_dy;
    double      m_loss = 0;
    double      m_frames = 0;
    RealType    m_scale;
    RealType    m_offset;

    struct create_t {
        RealType    scale  = (RealType)1.0;
        RealType    offset = (RealType)0.0;
    };

protected:
    LossLevelEncode(create_t const &create)
    {
        m_scale  = create.scale;
        m_offset = create.offset;
    }

public:
    ~LossLevelEncode() {}

    static std::shared_ptr<LossLevelEncode> Create(create_t const &create)
    {
        return std::shared_ptr<LossLevelEncode>(new LossLevelEncode(create));
    }
    
    static std::shared_ptr<LossLevelEncode> Create(RealType scale = (RealType)1.0, RealType offset = (RealType)0.0)
    {
        create_t create;
        create.scale  = scale;
        create.offset = offset;
        return Create(create);
    }

    static std::shared_ptr<LossLevelEncode> CreateEx(RealType scale = (RealType)1.0, RealType offset = (RealType)0.0)
    {
        create_t create;
        create.scale  = scale;
        create.offset = offset;
        return Create(create);
    }

    void Clear(void)
    {
        m_loss = 0;
        m_frames = 0;
    }

    double GetLoss(void) const 
    {
        return m_loss / m_frames;
    }

    FrameBuffer CalculateLoss(FrameBuffer y, FrameBuffer t, index_t batch_size)
    {
        index_t frame_size  = y.GetFrameSize();
        index_t y_node_size = y.GetNodeSize();
        index_t t_node_size = t.GetNodeSize();

        BB_ASSERT(frame_size == t.GetFrameSize());
        BB_ASSERT(y_node_size % t_node_size == 0);

        int         level_size = (int)(y_node_size / t_node_size);
        RealType    level_step = (RealType)1.0 / (RealType)(level_size + 1);

        m_dy.Resize(frame_size, {y_node_size}, DataType<RealType>::type);

        auto y_ptr = y.LockConst<BinType>();
        auto t_ptr = t.LockConst<RealType>();
        auto dy_ptr = m_dy.Lock<RealType>();

        for (index_t frame = 0; frame < frame_size; ++frame) {
            for (index_t node = 0; node < t_node_size; ++node) {
                RealType t  = (t_ptr.Get(frame, node) - m_offset) * m_scale;
                RealType th = level_step;
                for ( int i = 0; i < level_size; ++i ) {
                    RealType target = (t > th) ? (RealType)1.0 : (RealType)0.0;
                    RealType y      = y_ptr.Get(frame, node*level_size+i);
                    auto grad = y - target;
                    dy_ptr.Set(frame, node*level_size+i, grad / (RealType)batch_size);
                    auto error = grad * grad;
                    m_loss += error / (double)t_node_size;

                    th += level_step;
                }
            }
        }
        m_frames += frame_size;

        return m_dy;
    }
};


}

