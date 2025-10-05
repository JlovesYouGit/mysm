// VirtualSIMMobile.js - React Native Component
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, FlatList, StyleSheet } from 'react-native';
import { auth, db } from './firebase-config';
import { collection, addDoc, onSnapshot, query, where, orderBy } from 'firebase/firestore';

const VirtualSIMMobile = () => {
  const [user, setUser] = useState(null);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [simRegistered, setSimRegistered] = useState(false);
  const [simId, setSimId] = useState('');
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [recipient, setRecipient] = useState('');

  // Authenticate user
  useEffect(() => {
    // In a real app, you'd handle user auth properly
    const unsubscribe = auth.onAuthStateChanged(user => {
      if (user) {
        setUser(user);
        loadUserSIM(user.uid);
      }
    });
    
    return unsubscribe;
  }, []);

  // Load user's virtual SIM
  const loadUserSIM = async (userId) => {
    try {
      const q = query(collection(db, 'virtual_sims'), where('user_id', '==', userId));
      const unsubscribe = onSnapshot(q, (querySnapshot) => {
        querySnapshot.forEach((doc) => {
          const simData = doc.data();
          setSimRegistered(true);
          setSimId(simData.sim_id);
          setPhoneNumber(simData.phone_number);
          listenForMessages(simData.phone_number);
        });
      });
    } catch (error) {
      console.error('Error loading SIM:', error);
    }
  };

  // Listen for incoming messages
  const listenForMessages = (phoneNumber) => {
    const q = query(
      collection(db, 'sms_messages'),
      where('to', '==', phoneNumber),
      orderBy('timestamp', 'desc')
    );
    
    const unsubscribe = onSnapshot(q, (querySnapshot) => {
      const msgs = [];
      querySnapshot.forEach((doc) => {
        msgs.push({ id: doc.id, ...doc.data() });
      });
      setMessages(msgs);
    });
  };

  // Register virtual SIM
  const registerVirtualSIM = async () => {
    if (!user || !phoneNumber) return;
    
    try {
      // In a real implementation, this would call your backend
      // to register the virtual SIM with proper encryption
      const response = await fetch('http://your-server.com/api/register-virtual-sim', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${await user.getIdToken()}`
        },
        body: JSON.stringify({
          user_id: user.uid,
          phone_number: phoneNumber,
          encryption_key: generateEncryptionKey() // Generate secure key
        })
      });
      
      const data = await response.json();
      if (data.sim_id) {
        setSimId(data.sim_id);
        setSimRegistered(true);
        listenForMessages(phoneNumber);
      }
    } catch (error) {
      console.error('Error registering SIM:', error);
    }
  };

  // Send SMS
  const sendSMS = async () => {
    if (!recipient || !newMessage || !simRegistered) return;
    
    try {
      await addDoc(collection(db, 'sms_messages'), {
        from: phoneNumber,
        to: recipient,
        message: newMessage,
        timestamp: new Date(),
        status: 'sent',
        via: 'virtual_sim'
      });
      
      setNewMessage('');
    } catch (error) {
      console.error('Error sending SMS:', error);
    }
  };

  // Generate encryption key (simplified)
  const generateEncryptionKey = () => {
    return Math.random().toString(36).substring(2, 15) + 
           Math.random().toString(36).substring(2, 15);
  };

  if (!user) {
    return (
      <View style={styles.container}>
        <Text>Please log in to use Virtual SIM</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {!simRegistered ? (
        <View>
          <Text>Register Virtual SIM</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter phone number"
            value={phoneNumber}
            onChangeText={setPhoneNumber}
            keyboardType="phone-pad"
          />
          <Button title="Register SIM" onPress={registerVirtualSIM} />
        </View>
      ) : (
        <View style={styles.mainContainer}>
          <Text style={styles.header}>Virtual SIM Active</Text>
          <Text>Phone Number: {phoneNumber}</Text>
          <Text>SIM ID: {simId.substring(0, 8)}...</Text>
          
          <View style={styles.sendMessageContainer}>
            <TextInput
              style={styles.input}
              placeholder="Recipient"
              value={recipient}
              onChangeText={setRecipient}
              keyboardType="phone-pad"
            />
            <TextInput
              style={[styles.input, styles.messageInput]}
              placeholder="Message"
              value={newMessage}
              onChangeText={setNewMessage}
              multiline
            />
            <Button title="Send SMS" onPress={sendSMS} />
          </View>
          
          <Text style={styles.messagesHeader}>Messages</Text>
          <FlatList
            data={messages}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <View style={styles.messageItem}>
                <Text>From: {item.from}</Text>
                <Text>{item.message}</Text>
                <Text style={styles.timestamp}>
                  {item.timestamp?.toDate().toLocaleString()}
                </Text>
              </View>
            )}
          />
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff'
  },
  mainContainer: {
    flex: 1
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    marginBottom: 10,
    borderRadius: 5
  },
  messageInput: {
    height: 80,
    textAlignVertical: 'top'
  },
  sendMessageContainer: {
    marginBottom: 20
  },
  messagesHeader: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10
  },
  messageItem: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee'
  },
  timestamp: {
    fontSize: 12,
    color: '#666',
    marginTop: 5
  }
});

export default VirtualSIMMobile;