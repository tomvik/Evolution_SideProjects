import tensorflow as tf

hello = tf.constant('be fast')
sess = tf.Session()
print(sess.run(hello))