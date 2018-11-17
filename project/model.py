import tensorflow as tf
import numpy as np 
import os
import gym


class ADP_agent(object):
    def __init__(self,w_initializer=tf.contrib.layers.xavier_initializer(),b_initializer=tf.zeros_initializer(),U_c=0,gamma=1):
        self.U_c=U_c
        self.w_initializer=w_initializer
        self.b_initializer=b_initializer
        self.x=tf.placeholder(tf.float32,[1,4],name="input_x")
        self.gamma=gamma
    def goal_init(self):
        
        # implement goal network
        a_last=tf.placeholder(tf.float32,[1,1],name="action_t-1")
        self.g_input=tf.concat([self.x,a_last],axis=1)
        with tf.variable_scope("goal_network"):
            weights_1= tf.get_variable("gn_01_w",[5,5],initializer=self.w_initializer) #dimensions : [input layer, hidden_layer]
            bias_1 = tf.get_variable("gn_01_b",[5],initializer=self.b_initializer)#dimensions : [hidden_layer]
            tensor=tf.add(tf.matmul(self.g_input,weights_1),bias_1)
            tensor=tf.nn.relu(tensor) #dont know, assume it is relu
            weights_2= tf.get_variable("gn_02_w",[5,1],initializer=self.w_initializer)#dimensions : [hidden_layer,output_layer]
            bias_2 = tf.get_variable("gn_02_b",[1],initializer=self.b_initializer)#dimensions : [output_layer]
            tensor=tf.add(tf.matmul(tensor,weights_2),bias_2)
            self.s_now=tf.nn.sigmoid(tensor)
            #self.loss_goal=0.5*tf.squared_difference(self.V_now,self.U_c) # The value here is it the value from last time?
        print("goal network init finish")

    def critic_init(self):
        # implement critic network
        c_input=tf.concat([self.g_input,self.s_now],axis=1)
        with tf.variable_scope("critic_network"):
            weights_1= tf.get_variable("cn_01_w",[6,5],initializer=self.w_initializer)
            bias_1 = tf.get_variable("cn_01_b",[5],initializer=self.b_initializer)
            tensor=tf.add(tf.matmul(c_input,weights_1),bias_1)
            tensor=tf.nn.relu(tensor) #dont know, assume it is relu
            weights_2= tf.get_variable("cn_02_w",[5,1],initializer=self.w_initializer)
            bias_2 = tf.get_variable("cn_02_b",[1],initializer=self.b_initializer)
            tensor=tf.add(tf.matmul(tensor,weights_2),bias_2)
            self.V_now=tf.nn.sigmoid(tensor)
            V_last=tf.placeholder(tf.float32,[1,1],name="V_t-1")
            S_last=tf.placeholder(tf.float32,[1,1],name="S_t-1")
            #self.loss_critic=0.5*tf.squared_difference(gamma*V_now,(V_last-S_last))
        print("critic network init finish")
    def action_init(self):
        #  implement action network
        with tf.variable_scope("action_network"):
            weights_1= tf.get_variable("an_01_w",[4,5],initializer=self.w_initializer)
            bias_1 = tf.get_variable("an_01_b",[5],initializer=self.b_initializer)
            tensor=tf.add(tf.matmul(self.x,weights_1),bias_1)
            tensor=tf.nn.relu(tensor) #dont know, assume it is relu
            weights_2= tf.get_variable("an_02_w",[5,1],initializer=self.w_initializer)
            bias_2 = tf.get_variable("an_02_b",[1],initializer=self.b_initializer)
            tensor=tf.add(tf.matmul(tensor,weights_2),bias_2)
            a_now=tf.nn.sigmoid(tensor)
            #self.loss_action=0.5*tf.squared_difference(V,self.U_c)
        print("action network init finish")
    def test(self):
        action_var= tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='action_network')
        init = tf.initialize_all_variables()
        with tf.Session() as sess:
            sess.run(init)
            var=sess.run(action_var)
            print(var)


"""
    def run(self,T_a=,T_c=,T_g=,max_run=,N_a,N_c,N_g):
		optimizer_goal= tf.train.AdamOptimizer(learning_rate=learning_rate) 
        optimizer_action= tf.train.AdamOptimizer(learning_rate=learning_rate) 
        optimizer_critic= tf.train.AdamOptimizer(learning_rate=learning_rate) 
        opt_goal = optimizer.minimize(loss_goal)
        opt_action = optimizer.minimize(loss_action)
        opt_critic = optimizer.minimize(loss_critic)
        init = tf.initialize_all_variables()
        with tf.Session() as sess:
        ob_lst,reward_lst,done_lst,reward_s_lst=[],[],[],[]
            for i in range(max_run):
                sess.run(init)
                observation, reward, done, info = env.step(action)
                # implement goal network
                loss_goal=sess.run(loss_goal,feed_dict={})
                while (loss_goal > T_g) and (i < N):
                    _,s_now=sess.run([opt_goal,s_now],feed_dict={})
                    reward_s_lst.append(s_now)
                while (loss_goal > T_g) and (i < N):
                    _,s_now=sess.run([opt_goal,s_now],feed_dict={})
                    reward_s_lst.append(s_now)
                while (loss_goal > T_g) and (i < N):
                    _,s_now=sess.run([opt_goal,s_now],feed_dict={})
                    reward_s_lst.append(s_now)

"""






if __name__ == "__main__":
    agent=ADP_agent()
    agent.goal_init()
    agent.critic_init()
    agent.action_init()
    agent.test()
    """
    env = gym.make('CartPole-v0')

    env.reset()
    while random_episodes < 10:
        env.render()
        observation, reward, done, _ = env.step(np.random.randint(0,2))
        reward_sum += reward
        if done:
            random_episodes += 1
            print("Reward for this episode was:",reward_sum)
            reward_sum = 0
            env.reset()
    adp = ADP()
    adp.run()
    """
