import unittest
from unittest.mock import patch, MagicMock
import utils
import io

class TestATSGeneratorLLM(unittest.TestCase):
    
    @patch('utils.call_llm')
    def test_resume_generation_llm(self, mock_call_llm):
        # Mock LLM response
        mock_call_llm.return_value = "Optimized Summary\n- Experience Bullet 1"
        
        profile = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '123',
            'summary': 'Old Summary',
            'experience': 'Old Exp',
            'education': 'Edu',
            'skills': 'Skills'
        }
        job = {
            'title': 'Dev',
            'company': 'Tech',
            'description': 'Desc'
        }
        
        # Test with Mock Provider
        doc_stream = utils.generate_resume_docx(profile, job, "MockProvider", "key")
        
        self.assertIsNotNone(doc_stream)
        self.assertTrue(doc_stream.getbuffer().nbytes > 0)
        mock_call_llm.assert_called_once()

    @patch('utils.call_llm')
    def test_cover_letter_generation_llm(self, mock_call_llm):
        mock_call_llm.return_value = "Dear Hiring Manager,\nI am great."
        
        profile = {'name': 'Test', 'email': 'e', 'phone': 'p', 'summary': 's', 'experience': 'e'}
        job = {'title': 't', 'company': 'c', 'description': 'd'}
        
        doc_stream = utils.generate_cover_letter_docx(profile, job, "MockProvider", "key")
        
        self.assertIsNotNone(doc_stream)
        self.assertTrue(doc_stream.getbuffer().nbytes > 0)

if __name__ == '__main__':
    unittest.main()
