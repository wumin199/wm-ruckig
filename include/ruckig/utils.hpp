#pragma once

#include <array>
#include <string>
#include <sstream>
#include <iomanip>
#include <tuple>
#include <type_traits>
#include <vector>

namespace ruckig {


// @Status: √

// @Summary: 定义基本的数据类型和函数

//! Constant for indicating a dynamic (run-time settable) number of DoFs

// @Study: constexpr编译时就可以确定的自由度信息，具有组多好处如下：
/**
使用 constexpr 可以带来很多好处，包括：
在编译时就可以进行优化，提高代码的执行效率；
可以使用常量表达式来代替宏定义，提高代码的可读性和可维护性；
可以使用 constexpr 函数来编写泛型代码，使得代码更加通用。
*/
constexpr static size_t DynamicDOFs {0};


//! Vector data type based on the C++ standard library
// @Study: 自定义的StandardVector，根据DOFs的大学，其是std::array或者std::vector

/*
在 C++ 中，size_t 和 int 都是用于表示整数类型的数据类型，但它们在内存中的大小和取值范围等方面存在一些区别。

具体来说，size_t 是一个无符号整数类型，它的大小根据不同的编译器和操作系统可能会有所不同，但通常它的大小足够大，可以存储大部分对象的大小。在 32 位系统上，size_t 的大小通常为 4 字节，而在 64 位系统上，size_t 的大小通常为 8 字节。由于 size_t 是无符号整数类型，因此它的取值范围为 0 到 SIZE_MAX，其中 SIZE_MAX 是一个宏定义，表示 size_t 类型的最大值。

与之相比，int 是一个有符号整数类型，通常在 32 位系统上的大小为 4 字节，在 64 位系统上的大小为 4 或 8 字节。由于 int 是有符号整数类型，因此它的取值范围为 -INT_MAX 到 INT_MAX，其中 INT_MAX 是一个宏定义，表示 int 类型的最大值，而 -INT_MAX 则表示 int 类型的最小值。

在 C++ 中，通常使用 size_t 来表示对象的大小、数组的长度等非负整数，而使用 int 来表示有符号整数。在对数组进行遍历或者进行内存操作时，使用 size_t 可以避免发生内存溢出的问题。同时，由于 size_t 的取值范围更大，因此可以提高程序的可移植性。

*/

// @Study: std::conditional 是一个模板类，它可以根据一个布尔类型的条件来选择两个不同的类型。
// @Study: 通过使用 std::conditional 模板类，可以根据不同的条件选择不同的类型，从而实现更加灵活的类型定义。

/*
#include <iostream>
#include <type_traits>

template<typename T, typename U>
struct is_same_type {
    static constexpr bool value = std::is_same<T, U>::value;
    using type = typename std::conditional<value, T, U>::type;
};

int main() {
    std::cout << std::boolalpha;
    std::cout << is_same_type<int, int>::value << std::endl;  // true
    std::cout << is_same_type<int, double>::value << std::endl;  // false

    using result_type = is_same_type<int, double>::type;
    std::cout << std::is_same<result_type, double>::value << std::endl;  // true
    return 0;
}
*/

// @Study: 在 C++ 中，typename 是一个关键字，用于标识模板中的类型名称。
template<class T, size_t DOFs> using StandardVector = typename std::conditional<DOFs >= 1, std::array<T, DOFs>, std::vector<T>>::type;
template<class T, size_t DOFs, size_t SIZE> using StandardSizeVector = typename std::conditional<DOFs >= 1, std::array<T, SIZE>, std::vector<T>>::type;


//! Vector data type based on the Eigen matrix type. Eigen needs to be included seperately
// @Study: 判断是否有Eigen环境和版本
/*
EIGEN_VERSION_AT_LEAST 和 EIGEN_VERSION_AT_LEAST(x,y,z) 是两个不同的宏定义。

EIGEN_VERSION_AT_LEAST 是一个预定义的宏定义，它没有任何参数，用于判断是否定义了该宏定义。在 Eigen 矩阵库的头文件 Eigen/src/Core/util/Macros.h 中，该宏定义的定义方式如下：

#define EIGEN_VERSION_AT_LEAST

可以看到，该宏定义并没有任何实际的含义，只是用于判断是否定义了该宏定义。

EIGEN_VERSION_AT_LEAST(x,y,z) 是一个宏函数，它接受三个参数 x、y 和 z，分别表示 Eigen 矩阵库的主版本号、次版本号和修订号。该宏函数在 Eigen/src/Core/util/Macros.h 文件中被定义，用于判断当前版本号是否大于等于给定版本号，返回一个 bool 类型的值，用于条件编译。在使用该宏函数时，需要传入具体的版本号参数，例如：


#if EIGEN_VERSION_AT_LEAST(3,3,0)
    // Code for Eigen 3.3.0 or later
#else
    // Code for earlier versions of Eigen
#endif
可以看到，EIGEN_VERSION_AT_LEAST(x,y,z) 是一个有参数的宏函数，用于根据具体的版本号进行条件编译。

*/

#ifdef EIGEN_VERSION_AT_LEAST
#if EIGEN_VERSION_AT_LEAST(3,4,0)
    template<class T, size_t DOFs> using EigenVector = typename std::conditional<DOFs >= 1, Eigen::Vector<T, DOFs>, Eigen::Vector<T, Eigen::Dynamic>>::type;
#endif
#endif


// @Study: std::ostringstream 是 C++ 标准库中的一个输出流，它可以将输出的数据(int/double/str)以字符串的形式保存到内存中.

/**
与其他输出流相比，std::ostringstream 主要有以下优点：

方便转换：std::ostringstream 可以将输出的数据方便地转换成字符串，并保存到内存中。这对于需要将输出数据以字符串的形式保存到内存中的应用场景非常有用。
可重用性：std::ostringstream 可以多次使用，每次使用前只需要调用 str() 函数清空缓冲区即可，这使得开发人员可以方便地重复使用同一个对象。

*/

// @Study: std::setprecision(16) 表示输出的浮点数保留的小数位数为 16 位
template<class Vector>
inline std::string join(const Vector& array, size_t size) {
    std::ostringstream ss;
    for (size_t i = 0; i < size; ++i) {
        if (i) ss << ", ";
        ss << std::setprecision(16) << array[i];
    }
    return ss.str();
}


//! Integrate with constant jerk for duration t. Returns new position, new velocity, and new acceleration.

// @Study: 在const jerk的情况下，已知a0, v0, p0和j和t，求a, v, p
// @Study: 正向求导，反向积分

/*

在已知初加速度 a0，初速度 v0，初位置 p0，恒定加加速度（jerk）j 和时间 t 的情况下，我们可以使用以下公式来求解在时间 t 时的加速度 a、速度 v 和位置 p：

计算加速度 a：

a(t) = a0 + j * t   -> 求导

计算速度 v：

v(t) = v0 + a0 * t + 0.5 * j * t^2  -> 求导

计算位置 p：

p(t) = p0 + v0 * t + 0.5 * a0 * t^2 + (1/6) * j * t^3

将已知的 a0，v0，p0，j 和 t 值代入上述公式，即可求得 a，v 和 p 的值。


------

当然可以。我们将从基本的牛顿运动定律开始推导。

已知恒定加加速度（jerk）j，即加速度随时间的导数（a 的一阶导数）是常数。

计算加速度 a：
由于 jerk 是常数，我们可以通过对时间积分得到加速度公式：

a(t) = ∫j dt = j * t + C1

其中 C1 为积分常数。由已知条件，在 t=0 时，a(0) = a0，所以 C1 = a0。

因此，a(t) = a0 + j * t。

计算速度 v：
由于速度是加速度随时间的积分，我们再次对时间进行积分：

v(t) = ∫a(t) dt = ∫(a0 + j * t) dt

v(t) = a0 * t + (1/2) * j * t^2 + C2

其中 C2 为积分常数。由已知条件，在 t=0 时，v(0) = v0，所以 C2 = v0。

因此，v(t) = v0 + a0 * t + 0.5 * j * t^2。

计算位置 p：
同理，位置是速度随时间的积分，我们再次对时间进行积分：

p(t) = ∫v(t) dt = ∫(v0 + a0 * t + 0.5 * j * t^2) dt

p(t) = v0 * t + (1/2) * a0 * t^2 + (1/6) * j * t^3 + C3

其中 C3 为积分常数。由已知条件，在 t=0 时，p(0) = p0，所以 C3 = p0。

因此，p(t) = p0 + v0 * t + 0.5 * a0 * t^2 + (1/6) * j * t^3。

这样我们就得到了在已知初始条件下，求加速度 a、速度 v 和位置 p 的公式。


*/

inline std::tuple<double, double, double> integrate(double t, double p0, double v0, double a0, double j) {
    return std::make_tuple(
        p0 + t * (v0 + t * (a0 / 2 + t * j / 6)),
        v0 + t * (a0 + t * j / 2),
        a0 + t * j
    );
}

} // namespace ruckig
