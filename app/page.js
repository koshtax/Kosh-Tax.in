"use client";
import { useState } from 'react';
import Image from 'next/image';

export default function Home() {
  const [step, setStep] = useState(1);
  const [isClerkMode, setIsClerkMode] = useState(false);
  
  const [employerData, setEmployerData] = useState({
    tan: "CDHPP3301F",
    ddoName: "",
    schoolName: "Utkramit +2 High School, Tubil",
    ddoOffice: "K.B. +2 High School, Arki",
    treasury: "Khunti"
  });

  const [salaryData, setSalaryData] = useState({
    basic: 591000,
    da: 338860,
    hra: 59100,
    medical: 6000
  });

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header with Kosh-Tax Logo */}
      <header className="bg-teal text-white p-4 shadow-md flex justify-between items-center px-8">
        <div className="flex items-center gap-4">
          {/* Logo Integration */}
          <div className="bg-white p-1 rounded">
            <Image 
              src="/kosh-tax-logo.png" 
              alt="Kosh-Tax Logo" 
              width={140} 
              height={45} 
              priority
              className="object-contain h-10 w-auto"
            />
          </div>
          <h1 className="text-xl font-bold tracking-wide hidden sm:block border-l pl-4 border-teal-light">
            Form 16 Generator <span className="text-xs bg-teal-dark px-2 py-1 rounded ml-2">FY 2025-26</span>
          </h1>
        </div>
        <button className="text-sm underline hover:text-teal-light font-medium">Download Vault</button>
      </header>

      <main className="max-w-5xl mx-auto p-6 mt-8 w-full bg-white shadow-xl rounded-xl border-t-4 border-teal flex-grow mb-8">
        
        {/* Progress Navigation */}
        <div className="flex justify-between mb-8 border-b pb-4 text-sm font-bold text-gray-300">
          <span className={step >= 1 ? "text-teal" : ""}>1. Upload Slip</span>
          <span className={step >= 2 ? "text-teal" : ""}>2. Verify Data</span>
          <span className={step >= 3 ? "text-teal" : ""}>3. Draft Preview</span>
          <span className={step >= 4 ? "text-teal" : ""}>4. Payment</span>
        </div>

        {/* Step 1: Upload */}
        {step === 1 && (
          <div className="space-y-6 animate-fadeIn">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-teal-dark">Upload Salary Slip (Dec/Jan)</h2>
              <label className="flex items-center space-x-2 bg-teal-light/50 px-4 py-2 rounded-lg cursor-pointer border border-teal-light">
                <input type="checkbox" checked={isClerkMode} onChange={() => setIsClerkMode(!isClerkMode)} className="accent-teal w-4 h-4" />
                <span className="text-sm font-bold text-teal-dark">Clerk / Bulk Mode</span>
              </label>
            </div>
            
            <div className="border-2 border-dashed border-teal p-12 text-center rounded-lg bg-teal-light/20 hover:bg-teal-light/40 transition cursor-pointer">
              <div className="text-5xl mb-4">📄</div>
              <p className="font-bold text-slate text-lg">Drag & Drop your Salary Slip here</p>
              <p className="text-sm text-gray-500 mt-2">PDF, JPG, or PNG supported</p>
              <button onClick={() => setStep(2)} className="mt-6 px-8 py-3 bg-teal text-white font-bold rounded shadow-lg hover:bg-teal-dark transition">
                Start AI Extraction
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Verification */}
        {step === 2 && (
          <div className="space-y-8 animate-fadeIn">
            <h2 className="text-2xl font-bold text-teal-dark">Verify Extracted Data</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              
              <div className="space-y-4 bg-gray-50 p-6 rounded-lg border">
                <h3 className="font-bold text-slate border-b pb-2">Profile & DDO Mapping</h3>
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">School Name</label>
                  <input type="text" value={employerData.schoolName} onChange={(e) => setEmployerData({...employerData, schoolName: e.target.value})} className="w-full border p-2 rounded focus:ring-2 focus:ring-teal outline-none" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">DDO Office</label>
                  <input type="text" value={employerData.ddoOffice} onChange={(e) => setEmployerData({...employerData, ddoOffice: e.target.value})} className="w-full border p-2 rounded focus:ring-2 focus:ring-teal outline-none" />
                </div>
              </div>

              <div className="space-y-4 bg-gray-50 p-6 rounded-lg border">
                <h3 className="font-bold text-slate border-b pb-2">Financial Entries (Editable)</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1">Total Basic Pay</label>
                    <input type="number" value={salaryData.basic} onChange={(e) => setSalaryData({...salaryData, basic: Number(e.target.value)})} className="w-full border p-2 rounded font-mono focus:ring-2 focus:ring-teal outline-none" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1">Total DA</label>
                    <input type="number" value={salaryData.da} onChange={(e) => setSalaryData({...salaryData, da: Number(e.target.value)})} className="w-full border p-2 rounded font-mono focus:ring-2 focus:ring-teal outline-none" />
                  </div>
                </div>
              </div>
            </div>
            <button onClick={() => setStep(3)} className="w-full py-4 bg-teal text-white text-lg font-bold rounded shadow-lg hover:bg-teal-dark transition">
              Confirm & Generate Draft
            </button>
          </div>
        )}

        {/* Step 3: Draft Preview */}
        {step === 3 && (
          <div className="space-y-6 animate-fadeIn text-center">
            <h2 className="text-2xl font-bold text-teal-dark">Review Your Form 16</h2>
            <div className="relative border-4 border-gray-200 p-8 h-96 overflow-hidden bg-white shadow-inner flex flex-col items-center justify-center">
              <div className="absolute text-5xl md:text-7xl font-black text-red-500 opacity-10 transform -rotate-45 pointer-events-none whitespace-nowrap">
                DRAFT - NOT FOR OFFICIAL USE
              </div>
              <div className="text-left w-full max-w-md relative z-10 opacity-80 bg-white/50 p-6 rounded-lg backdrop-blur-sm border">
                <div className="mb-4 text-center border-b pb-4">
                  <Image src="/kosh-tax-logo.png" alt="Kosh-Tax" width={100} height={30} className="mx-auto mb-2 opacity-50" />
                  <p className="text-xs font-bold">Schedule of Income - Tax (Draft)</p>
                </div>
                <p className="flex justify-between border-b py-2"><strong>Gross Total Income:</strong> <span>₹{(salaryData.basic + salaryData.da + salaryData.hra + salaryData.medical).toLocaleString()}</span></p>
                <p className="flex justify-between border-b py-2"><strong>Standard Deduction:</strong> <span>₹75,000</span></p>
                <p className="mt-4 text-lg text-red-600 font-bold text-center">Calculated Tax (Feb): ₹40,083</p>
              </div>
            </div>
            <button onClick={() => setStep(4)} className="w-full py-4 bg-teal text-white text-lg font-bold rounded shadow-lg hover:bg-teal-dark transition">
              Looks Good, Proceed to Payment
            </button>
          </div>
        )}

        {/* Step 4: Payment */}
        {step === 4 && (
          <div className="space-y-6 animate-fadeIn max-w-md mx-auto text-center">
            <h2 className="text-2xl font-bold text-teal-dark">Complete Generation</h2>
            <div className="bg-slate text-white p-8 rounded-xl shadow-lg border-2 border-teal">
              <p className="mb-2 font-bold">Scan QR Code to pay ₹99</p>
              <div className="w-48 h-48 bg-white mx-auto mb-6 flex items-center justify-center text-slate font-bold rounded-lg">
                [ UPI QR CODE HERE ]
              </div>
              <div className="text-left">
                <label className="block text-xs font-bold text-teal-light mb-2">Enter UTR / Transaction ID</label>
                <input type="text" placeholder="e.g. 308412345678" className="w-full p-3 rounded text-slate font-mono font-bold focus:ring-4 focus:ring-teal outline-none" />
              </div>
              <button className="mt-6 w-full py-4 bg-teal text-white font-bold text-lg rounded shadow-lg hover:bg-teal-light hover:text-slate transition">
                Submit & Request PDF
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
