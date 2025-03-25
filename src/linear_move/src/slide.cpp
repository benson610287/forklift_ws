#include<iostream>
#include<modbus/modbus.h>
#include <unistd.h>

#include <memory>
#include "std_msgs/msg/int64.hpp"

// #include "../include/linear_move/slide.h"
#include <slide.h>
#include "rclcpp/rclcpp.hpp"
// #include "ros/ros.h"
#include "std_msgs/msg/string.hpp"

uint32_t read_feedback(modbus_t* ct,int ADDRESS_FDB,int FDB_LENGTH,uint16_t fdb_val[2])
{
    int rc = modbus_read_registers(ct, ADDRESS_FDB, FDB_LENGTH, fdb_val);
    if (rc != FDB_LENGTH)
    {
        fprintf(stderr, "modbus read failed: %d %s\n", errno, modbus_strerror(errno));
        errno = 0;
        return errno;
    }
    else {
        // Interpret the two consecutive registers as a 32-bit integer
        uint32_t value_32bit = (fdb_val[1] << 16) | fdb_val[0];
        // printf("32-bit value: %u\n", value_32bit);
        return value_32bit;
    }
    // std::cout<<std::endl;
}

void write_command(modbus_t* ct,int ADDRESS_CMD,int CMD_LENGTH,uint16_t cmd_arr[2])
{
    int rc = modbus_write_registers(ct, ADDRESS_CMD, CMD_LENGTH, cmd_arr);
    if (rc != CMD_LENGTH)
    {
        fprintf(stderr, "modbus write failed: %d %s\n", errno, modbus_strerror(errno));
        errno = 0;
    }
    std::cout << "write success" << std::endl;
}

modbus_t* init_modbus_rtu(int id, std::string port, int baud_rate)
{
    modbus_t* ct = modbus_new_rtu(port.c_str(), baud_rate, 'E', 8, id);
    modbus_set_slave(ct, 0x7F);
    if (modbus_connect(ct) == -1)
    {
        fprintf(stderr, "Connection failed: %s\n",
            modbus_strerror(errno));
        std::cout << "Error connect" << std::endl;
        modbus_free(ct);
        return nullptr;
    }
    std::cout << "Init success" << std::endl;
    // modbus_set_debug(ct, true);

    return ct;
}

int32_t conert_CM2PUU(int cm){
    if(-5<cm && cm<30){
        cm*=199031.975; //15922558/80=199031.975 (PUU/CM)
    }else{
        cm*=199031.975; //15922558/80=199031.975 (PUU/CM)
    }
    
    return int32_t(cm);
}
void transformPUU2path(int32_t PUU){
    int LOW_BIT=PUU;
    int HIGH_BIT=PUU;
    LOW_BIT=(LOW_BIT<<16)>>16;
    HIGH_BIT=(HIGH_BIT>>16);
    path_data[0]=LOW_BIT;
    path_data[1]=HIGH_BIT;
}
void working(modbus_t *ctx){
    std::cout<<"writing_servo_on"<<std::endl;
    write_command(ctx,Servo_on_Adress,Registers_Lenth,servo_on);
    std::cout<<"writing_jog_data"<<std::endl;
    write_command(ctx,jog_Adress,Registers_Lenth,jog_data);
    std::cout<<"writing_path_def"<<std::endl;
    write_command(ctx,path1_def_Address,Registers_Lenth,path_def);
    std::cout<<"writing_path_data"<<std::endl;
    write_command(ctx,path1_data_Address,Registers_Lenth,path_data);
    std::cout<<"reading_path1_def_Address"<<std::endl;
    read_feedback(ctx,path1_def_Address,Registers_Lenth,dest);
    std::cout<<"reading_path1_data_Address"<<std::endl;
    read_feedback(ctx,path1_data_Address,Registers_Lenth,dest);
    std::cout<<"writing_move_point"<<std::endl;
    write_command(ctx,move_Address,Registers_Lenth,move_point);
    std::cout<<"writing_servo_on"<<std::endl;
    while(read_feedback(ctx,move_Address,Registers_Lenth,dest)<20000){
        continue;
    }
    std::cout<<"writing_servo_off"<<std::endl;
    write_command(ctx,Servo_on_Adress,Registers_Lenth,servo_off);
}


void chatterCallback(const std_msgs::msg::Int64 msg)
{
    
    // RCLCPP_INFO(node->get_logger(),"I heard: [%ld]", msg.data);
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "I heard: [%ld]", msg.data);
    modbus_t *ctx=init_modbus_rtu(1,"/dev/ttyUSB1",9600);
    int32_t PUU=conert_CM2PUU(msg.data);
    transformPUU2path(PUU);
    working(ctx);
    modbus_close(ctx);
    modbus_free(ctx);
}

int main(int argc, char **argv)
{
    

//   ros::init(argc, argv, "listener");
    rclcpp::init(argc, argv);

    std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("add_two_ints_server");

    // ros::NodeHandle n;
    rclcpp::Subscription<std_msgs::msg::Int64>::SharedPtr sub = node->create_subscription<std_msgs::msg::Int64>("topic", 1000, chatterCallback);
    // ros::Subscriber sub = n.subscribe("topic", 1000, chatterCallback);

    rclcpp::spin(node);




  return 0;
}